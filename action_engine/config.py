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

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv('ACCESS_TOKEN_EXPIRE_SECONDS', '3600'))
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'enc_key')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')


def get_oauth_config(platform: str) -> dict:
    """Return OAuth configuration values for a given platform."""
    prefix = platform.upper()
    return {
        'client_id': os.getenv(f'{prefix}_CLIENT_ID', ''),
        'client_secret': os.getenv(f'{prefix}_CLIENT_SECRET', ''),
        'redirect_uri': os.getenv(f'{prefix}_REDIRECT_URI', ''),
        'scope': os.getenv(f'{prefix}_SCOPE', ''),
    }
