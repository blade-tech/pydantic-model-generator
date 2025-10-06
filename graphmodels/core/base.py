"""Base Pydantic models with strict validation and shared enums."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProvenanceSystem(str, Enum):
    """System of origin for provenance tracking."""

    SLACK = "slack"
    AAOIFI = "aaoifi"
    FIBO = "fibo"
    CUSTOM = "custom"
    UNKNOWN = "unknown"


class Currency(str, Enum):
    """Supported currency codes."""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    SAR = "SAR"


class PriorityLevel(str, Enum):
    """Priority levels for projects/tasks."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ModelBase(BaseModel):
    """Strict base model for all Pydantic V2 models.

    Configuration:
    - Forbid extra fields to catch typos/schema drift
    - Strict validation for type safety
    - Use enum values for serialization
    - Validate assignment for runtime safety
    """

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        use_enum_values=True,
        validate_assignment=True,
    )
