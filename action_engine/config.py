import os
from pathlib import Path

# Load variables from .env if present
_env_path = Path(__file__).resolve().parent.parent / '.env'
if _env_path.exists():
    with _env_path.open() as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

API_KEY = os.getenv('API_KEY', 'testkey')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
