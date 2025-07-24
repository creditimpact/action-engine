from typing import Dict

_ENGINE_CONFIGS: Dict[str, Dict] = {}


def set_engine_config(engine_id: str, config: Dict) -> None:
    """Store configuration for an engine."""
    _ENGINE_CONFIGS[engine_id] = config


def get_engine_config(engine_id: str) -> Dict:
    """Return configuration for an engine or empty dict."""
    return _ENGINE_CONFIGS.get(engine_id, {})


def clear_engine_configs() -> None:
    """Remove all configs (mainly for tests)."""
    _ENGINE_CONFIGS.clear()
