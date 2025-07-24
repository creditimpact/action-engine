"""Models related to platform metadata."""

from __future__ import annotations

from pydantic import BaseModel


class PlatformStatus(BaseModel):
    platform: str
    status: str


class PlatformListResponse(BaseModel):
    platforms: dict
