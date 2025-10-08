"""Core base model configuration."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, RootModel
from typing import Any


class ConfiguredBaseModel(BaseModel):
    """
    Base model with Pydantic v2 configuration.
    All generated models inherit this configuration.
    """
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class LinkMLMeta(RootModel):
    """LinkML metadata container."""
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root
