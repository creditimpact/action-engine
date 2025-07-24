"""Pydantic models for engine-related operations."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel


class EngineRegistration(BaseModel):
    engine_id: str
    permissions: Dict[str, Dict[str, List[str]]]
    depends_on: Optional[List[str]] = None


class EngineValidation(BaseModel):
    engine_id: str
    engine_key: str
