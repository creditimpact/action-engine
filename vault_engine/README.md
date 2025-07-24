# Vault Engine

Vault Engine is a simple token storage service used alongside the Action Engine. It stores OAuth tokens encrypted in Redis and exposes a small HTTP API for retrieving them.

## Required environment variables

- `VAULT_REDIS_URL` – connection string for the Redis instance where encrypted tokens are stored.
- `VAULT_ENCRYPTION_KEY` – 32‑byte key used for AES‑256‑CBC encryption.
- `VAULT_ENCRYPTION_IV` – 16‑byte initialization vector for encryption.
- `ACTION_ENGINE_KEY` – shared key for the action engine.
- `SYNC_ENGINE_KEY` – shared key for the sync engine.
- `LOCAL_ENGINE_KEY` – shared key for local/testing access.

These engine keys are validated via the `X-Engine-ID` and `X-Engine-Key` headers on every request.

## API usage

Tokens are typically obtained from the Action Engine's OAuth flow described in the [project README](../README.md#initiating-oauth). Once retrieved you can store and fetch them using the following endpoints.

### Store token

```bash
curl -X POST http://localhost:8000/store_token \
     -H "X-Engine-ID: action" \
     -H "X-Engine-Key: $ACTION_ENGINE_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "user_id": "u1",
           "platform": "google",
           "access_token": "...",
           "refresh_token": "...",
           "expires_at": 1234567890,
           "scopes": ["email"]
         }'
```

### Get token

```bash
curl -X POST "http://localhost:8000/get_token?user_id=u1&platform=google" \
     -H "X-Engine-ID: action" \
     -H "X-Engine-Key: $ACTION_ENGINE_KEY"
```

### Connection status

```bash
curl -X POST "http://localhost:8000/status?user_id=u1" \
     -H "X-Engine-ID: action" \
     -H "X-Engine-Key: $ACTION_ENGINE_KEY"
```

All endpoints return JSON responses indicating success or containing the requested token information.
