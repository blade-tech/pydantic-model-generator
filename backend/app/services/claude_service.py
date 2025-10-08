"""Claude AI service for ontology research and generation.

This service uses the Anthropic API to:
1. Analyze business text and identify entities
2. Map entities to canonical ontologies (DoCO, FaBiO, PROV-O, FIBO, SKOS)
3. Generate OutcomeSpecs
4. Generate LinkML schemas

NO MOCKS - Real Anthropic API calls with streaming support.
"""

import logging
from typing import List, Dict, Any, AsyncGenerator, Optional
import anthropic
from app.models.schemas import EntityMapping
from app.prompts import (
    build_ontology_research_prompt,
    build_outcome_spec_prompt,
    build_linkml_schema_prompt,
)

logger = logging.getLogger(__name__)


class ClaudeService:
    """Service for Claude AI interactions."""

    def __init__(self, api_key: str, model: str, max_tokens: int, temperature: float):
        """Initialize Claude service.

        Args:
            api_key: Anthropic API key
            model: Claude model name (e.g., 'claude-3-5-sonnet-20241022')
            max_tokens: Maximum tokens for responses
            temperature: Temperature for generation (0.0-1.0)
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        logger.info(f"Initialized Claude service with model: {model}")

    async def research_ontologies(
        self,
        business_text: str,
        user_context: Optional[str] = None,
        use_mcp_tools: bool = False,
        custom_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Research ontologies for business text with streaming.

        This streams Claude's thinking process as it:
        1. Analyzes the business text
        2. Identifies 2-8 key entities
        3. Maps each entity to canonical ontology URIs
        4. Provides confidence scores and reasoning

        Args:
            business_text: Business outcome description
            user_context: Optional user context, instructions, or domain knowledge
            use_mcp_tools: Whether to enable MCP tools (web search, docs lookup)
            custom_prompt: Optional custom prompt template (overrides default)

        Yields:
            Streaming chunks of Claude's reasoning
        """
        # Build the prompt using the prompt builder
        prompt = build_ontology_research_prompt(
            business_text=business_text,
            user_context=user_context,
            use_mcp_tools=use_mcp_tools,
            custom_prompt=custom_prompt
        )

        try:
            # Stream Claude's response
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Claude API error: {e}", exc_info=True)
            raise

    async def generate_outcome_spec(
        self,
        business_text: str,
        entities: List[EntityMapping],
        custom_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Generate OutcomeSpec YAML with streaming.

        Args:
            business_text: Business outcome description
            entities: Identified entities with ontology mappings
            custom_prompt: Optional custom prompt template

        Yields:
            Streaming chunks of Claude's thinking
        """
        entities_str = "\n".join([
            f"- {e.entity_name} ({e.entity_type}): {e.ontology_uri}"
            for e in entities
        ])

        prompt = build_outcome_spec_prompt(
            business_text=business_text,
            entities_str=entities_str,
            custom_prompt=custom_prompt
        )

        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Claude API error: {e}", exc_info=True)
            raise

    async def generate_linkml_schema(
        self,
        outcome_spec: Dict[str, Any],
        entities: List[EntityMapping],
        custom_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Generate LinkML schema YAML with streaming.

        Args:
            outcome_spec: Generated OutcomeSpec
            entities: Identified entities with ontology mappings
            custom_prompt: Optional custom prompt template

        Yields:
            Streaming chunks of Claude's thinking
        """
        entities_str = "\n".join([
            f"- {e.entity_name} ({e.entity_type}): {e.ontology_uri}"
            for e in entities
        ])

        prompt = build_linkml_schema_prompt(
            outcome_spec=str(outcome_spec),
            entities_str=entities_str,
            custom_prompt=custom_prompt
        )

        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Claude API error: {e}", exc_info=True)
            raise
