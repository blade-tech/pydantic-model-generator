"""Ontology retriever using Exa and Firecrawl APIs.

For MVP: Fail explicitly if API keys missing. No silent fallbacks.
"""

import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
import httpx

load_dotenv()


class OntologyRetrieverError(Exception):
    """Raised when ontology retrieval fails."""

    pass


class OntologyRetriever:
    """Retrieves ontology definitions using Exa and Firecrawl.

    For MVP:
    - Requires EXA_API_KEY and FIRECRAWL_API_KEY in .env
    - Fails explicitly with actionable error messages
    - No silent fallbacks or degraded modes
    """

    def __init__(self):
        self.exa_api_key = os.getenv("EXA_API_KEY")
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

        if not self.exa_api_key:
            raise OntologyRetrieverError(
                "EXA_API_KEY not found in environment. "
                "Add to .env file or set environment variable."
            )

        if not self.firecrawl_api_key:
            raise OntologyRetrieverError(
                "FIRECRAWL_API_KEY not found in environment. "
                "Add to .env file or set environment variable."
            )

        self.exa_url = "https://api.exa.ai/search"
        self.firecrawl_url = "https://api.firecrawl.dev/v0/scrape"

    async def search_ontology(
        self,
        prefix: str,
        base_uri: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """Search for ontology documentation using Exa.

        Args:
            prefix: Ontology prefix (e.g., "dcterms", "doco")
            base_uri: Base URI (e.g., "http://purl.org/dc/terms/")
            max_results: Maximum results to return

        Returns:
            List of search results with URLs and snippets

        Raises:
            OntologyRetrieverError: If search fails
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.exa_url,
                    headers={
                        "Authorization": f"Bearer {self.exa_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "query": f"{prefix} ontology documentation {base_uri}",
                        "num_results": max_results,
                        "type": "neural",
                        "contents": {"text": True, "highlights": True},
                    },
                )
                response.raise_for_status()
                data = response.json()

                return [
                    {
                        "url": result["url"],
                        "title": result.get("title", ""),
                        "snippet": result.get("text", ""),
                        "highlights": result.get("highlights", []),
                    }
                    for result in data.get("results", [])
                ]

        except httpx.HTTPError as e:
            raise OntologyRetrieverError(
                f"Exa search failed for {prefix}: {str(e)}"
            ) from e

    async def scrape_ontology_page(self, url: str) -> Dict[str, Any]:
        """Scrape ontology documentation page using Firecrawl.

        Args:
            url: URL to scrape

        Returns:
            Scraped content including text and metadata

        Raises:
            OntologyRetrieverError: If scraping fails
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.firecrawl_url,
                    headers={
                        "Authorization": f"Bearer {self.firecrawl_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "url": url,
                        "formats": ["markdown", "html"],
                        "onlyMainContent": True,
                    },
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "url": url,
                    "markdown": data.get("data", {}).get("markdown", ""),
                    "html": data.get("data", {}).get("html", ""),
                    "metadata": data.get("data", {}).get("metadata", {}),
                }

        except httpx.HTTPError as e:
            raise OntologyRetrieverError(
                f"Firecrawl scrape failed for {url}: {str(e)}"
            ) from e

    async def retrieve_ontologies(
        self,
        ontology_hints: List[Dict[str, str]],
        output_path: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Retrieve ontology documentation for all hints.

        Args:
            ontology_hints: List of {prefix, base_uri} dicts from OutcomeSpec
            output_path: Optional path to save results as JSON

        Returns:
            Dictionary mapping prefix -> ontology data

        Example:
            >>> hints = [
            ...     {"prefix": "dcterms", "base_uri": "http://purl.org/dc/terms/"},
            ...     {"prefix": "doco", "base_uri": "http://purl.org/spar/doco/"}
            ... ]
            >>> results = await retriever.retrieve_ontologies(hints)
        """
        results = {}

        for hint in ontology_hints:
            prefix = hint["prefix"]
            base_uri = hint["base_uri"]

            print(f"Searching ontology: {prefix} ({base_uri})")

            # Search for ontology docs
            search_results = await self.search_ontology(prefix, base_uri)

            if not search_results:
                print(f"  Warning: No results found for {prefix}")
                results[prefix] = {
                    "base_uri": base_uri,
                    "search_results": [],
                    "scraped_pages": [],
                }
                continue

            # Scrape top result
            top_url = search_results[0]["url"]
            print(f"  Scraping: {top_url}")

            try:
                scraped = await self.scrape_ontology_page(top_url)
                results[prefix] = {
                    "base_uri": base_uri,
                    "search_results": search_results,
                    "scraped_pages": [scraped],
                }
            except OntologyRetrieverError as e:
                print(f"  Warning: Scrape failed - {e}")
                results[prefix] = {
                    "base_uri": base_uri,
                    "search_results": search_results,
                    "scraped_pages": [],
                }

        # Save to file if path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\nSaved ontology references to: {output_path}")

        return results


async def retrieve_ontologies_for_outcome(
    outcome_spec_path: Path,
    output_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Convenience function to retrieve ontologies from OutcomeSpec.

    Args:
        outcome_spec_path: Path to OutcomeSpec YAML
        output_path: Optional path to save results

    Returns:
        Ontology retrieval results

    Raises:
        OntologyRetrieverError: If retrieval fails
    """
    from dsl.loader import load_outcome_spec

    # Load OutcomeSpec
    spec = load_outcome_spec(outcome_spec_path)

    # Extract ontology hints
    ontology_hints = [
        {"prefix": ont.prefix, "base_uri": ont.base_uri} for ont in spec.ontologies
    ]

    if not ontology_hints:
        print("No ontology hints in OutcomeSpec - skipping ontology retrieval")
        return {}

    # Retrieve ontologies
    retriever = OntologyRetriever()
    return await retriever.retrieve_ontologies(ontology_hints, output_path)
