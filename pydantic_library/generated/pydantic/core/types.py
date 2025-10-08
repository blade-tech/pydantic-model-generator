"""Core custom types for validation."""
from __future__ import annotations

import re
from typing import Annotated
from pydantic import Field, field_validator, BaseModel

# Email type with validation
Email = Annotated[
    str,
    Field(pattern=r'^[^@\s]+@[^@\s]+\.[^@\s]+$', description="Email address with basic validation")
]

# E.164 Phone number format
E164Phone = Annotated[
    str,
    Field(pattern=r'^\+?[1-9]\d{7,15}$', description="E.164 phone number format (international)")
]

# Confidence score between 0 and 1
Confidence01 = Annotated[
    float,
    Field(ge=0, le=1, description="Confidence score between 0 and 1")
]
