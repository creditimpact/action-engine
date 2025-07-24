"""Miscellaneous helper utilities used across the engine."""

from __future__ import annotations

from typing import Any, Dict


def merge_dicts(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Return a new dictionary containing ``a`` updated with ``b``."""

    result = dict(a)
    result.update(b)
    return result

