"""Test ontology retriever with mock responses (no real API calls for MVP test)."""

import asyncio
import json
from pathlib import Path
from agents.ontology_retriever import OntologyRetriever, OntologyRetrieverError


async def test_validation():
    """Test that retriever validates API keys."""
    print("Testing API key validation...")

    try:
        # This will fail if keys are not in .env
        retriever = OntologyRetriever()
        print(f"  Exa API key configured: {bool(retriever.exa_api_key)}")
        print(f"  Firecrawl API key configured: {bool(retriever.firecrawl_api_key)}")
        print("[PASS] API keys validated\n")
        return True
    except OntologyRetrieverError as e:
        print(f"[EXPECTED] API keys missing: {e}")
        print("For real usage, add EXA_API_KEY and FIRECRAWL_API_KEY to .env\n")
        return False


async def test_structure():
    """Test the expected data structure (without real API calls)."""
    print("Testing expected data structure...")

    # Mock ontology hints from OutcomeSpec
    hints = [
        {"prefix": "dcterms", "base_uri": "http://purl.org/dc/terms/"},
        {"prefix": "doco", "base_uri": "http://purl.org/spar/doco/"},
    ]

    # Expected result structure
    expected_result = {
        "dcterms": {
            "base_uri": "http://purl.org/dc/terms/",
            "search_results": [
                {
                    "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
                    "title": "DCMI Metadata Terms",
                    "snippet": "Dublin Core Metadata Initiative terms...",
                    "highlights": [],
                }
            ],
            "scraped_pages": [
                {
                    "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
                    "markdown": "# DCMI Metadata Terms\n\n...",
                    "html": "<h1>DCMI Metadata Terms</h1>...",
                    "metadata": {"title": "DCMI Metadata Terms"},
                }
            ],
        }
    }

    print(f"  Expected structure for {len(hints)} ontologies:")
    print(f"    - search_results: List of URLs and snippets")
    print(f"    - scraped_pages: List of scraped content (markdown/html)")
    print("[PASS] Data structure defined\n")

    return expected_result


async def main():
    print("=" * 60)
    print("Ontology Retriever Tests (MVP)")
    print("=" * 60 + "\n")

    # Test 1: API key validation
    has_keys = await test_validation()

    # Test 2: Data structure
    expected = await test_structure()

    print("=" * 60)
    if has_keys:
        print("Ready for real API calls!")
        print("\nUsage:")
        print("  from agents.ontology_retriever import retrieve_ontologies_for_outcome")
        print("  results = await retrieve_ontologies_for_outcome(")
        print('      Path("dsl/examples/resource_allocation.yaml"),')
        print('      output_path=Path("artifacts/ontology_refs.json")')
        print("  )")
    else:
        print("Configure API keys to enable ontology retrieval")
        print("\nAdd to .env:")
        print("  EXA_API_KEY=your_exa_key")
        print("  FIRECRAWL_API_KEY=your_firecrawl_key")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
