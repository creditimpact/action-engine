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

# OAuth configuration for supported platforms
GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID', '')
GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET', '')
GMAIL_REDIRECT_URI = os.getenv('GMAIL_REDIRECT_URI', '')

GOOGLE_CALENDAR_CLIENT_ID = os.getenv('GOOGLE_CALENDAR_CLIENT_ID', '')
GOOGLE_CALENDAR_CLIENT_SECRET = os.getenv('GOOGLE_CALENDAR_CLIENT_SECRET', '')
GOOGLE_CALENDAR_REDIRECT_URI = os.getenv('GOOGLE_CALENDAR_REDIRECT_URI', '')

NOTION_CLIENT_ID = os.getenv('NOTION_CLIENT_ID', '')
NOTION_CLIENT_SECRET = os.getenv('NOTION_CLIENT_SECRET', '')
NOTION_REDIRECT_URI = os.getenv('NOTION_REDIRECT_URI', '')

ZAPIER_CLIENT_ID = os.getenv('ZAPIER_CLIENT_ID', '')
ZAPIER_CLIENT_SECRET = os.getenv('ZAPIER_CLIENT_SECRET', '')
ZAPIER_REDIRECT_URI = os.getenv('ZAPIER_REDIRECT_URI', '')
