"""Prompt templates for Claude AI services."""

from .templates import (
    ONTOLOGY_RESEARCH_SYSTEM,
    ONTOLOGY_RESEARCH_TASK,
    OUTCOME_SPEC_SYSTEM,
    OUTCOME_SPEC_TASK,
    LINKML_SCHEMA_SYSTEM,
    LINKML_SCHEMA_TASK,
    build_ontology_research_prompt,
    build_outcome_spec_prompt,
    build_linkml_schema_prompt,
)

__all__ = [
    "ONTOLOGY_RESEARCH_SYSTEM",
    "ONTOLOGY_RESEARCH_TASK",
    "OUTCOME_SPEC_SYSTEM",
    "OUTCOME_SPEC_TASK",
    "LINKML_SCHEMA_SYSTEM",
    "LINKML_SCHEMA_TASK",
    "build_ontology_research_prompt",
    "build_outcome_spec_prompt",
    "build_linkml_schema_prompt",
]
