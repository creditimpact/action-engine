"""Helpers for formatting action payloads."""

from __future__ import annotations

from typing import Any, Dict


def format_payload(platform: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return ``payload`` possibly transformed for ``platform``.

    Currently this function simply returns the payload unchanged but acts as a
    central place to apply any platform specific formatting rules in the
    future.
    """

    # Placeholder for platform specific formatting logic.
    return dict(payload)

