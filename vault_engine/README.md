# Vault Engine

The Vault is PURAIFI's secure storage service for all user-level authorization data. Other engines (such as the Action and Sync engines) rely on the Vault to access OAuth tokens and connection metadata without handling secrets directly.

## Overview & Role
- Stores encrypted OAuth access and refresh tokens along with platform scopes and expiration times.
- Maintains the connection status for each platform per user so other engines can determine if they can operate on the user's behalf.
- Provides a stateless REST API that only other engines may call. There are no direct user-facing endpoints.

## What It Stores
- OAuth tokens for Google, Slack, Notion and other platforms.
- Token expiry times and granted scopes.
- Per-user encryption keys and session information (never raw passwords).

## Core Functions
- Securely store and retrieve tokens.
- Refresh expired tokens when possible.
- Report the connection status of each platform for a user.
- Supply the Sync engine with an integration map describing which services are connected.

## API Responsibilities
All requests must include `X-Engine-ID` and `X-Engine-Key` headers identifying the calling engine. The current endpoints are:

| Method & Path      | Description                              |
|--------------------|------------------------------------------|
| `POST /store_token`| Store or update a token for a user.      |
| `POST /get_token`  | Retrieve (and refresh if needed) a token.|
| `GET  /status`     | Return connection status for each platform for a user.|
| *(internal)*       | Platform map generation for the Sync engine.|

Each endpoint returns a JSON response.

## Architecture
- Stateless FastAPI application.
- Authentication enforced by `auth_middleware.py` for each engine.
- Tokens stored in Redis and encrypted using AES‑256 via `token_encryptor.py`. The system is designed for a double layer of encryption so secrets never appear in plaintext.
- Access is separated per user and per platform key (`<user_id>:<platform>`).
- Extensive logging using `vault_logger.py` attaches a UUID request ID to every operation.

## Modules & Files
- `vault_api.py` – HTTP API definitions.
- `auth_middleware.py` – validates engine credentials for every request.
- `vault_storage.py` – Redis based encrypted token store.
- `token_encryptor.py` – AES encryption helper.
- `token_refresher.py` – refresh logic for expired tokens.
- `connection_checker.py` – determines connection health per platform.
- `vault_logger.py` – JSON logging with request ID context.
- `platform_profiles/` – YAML files describing OAuth details for supported platforms.

## Configuration
The service requires the following environment variables:

- `VAULT_REDIS_URL` – connection string for the Redis instance.
- `VAULT_ENCRYPTION_KEY` – 32‑byte key used for AES‑256 encryption.
- `VAULT_ENCRYPTION_IV` – 16‑byte initialization vector.
- `ACTION_ENGINE_KEY` – shared secret for the Action engine.
- `SYNC_ENGINE_KEY` – shared secret for the Sync engine.
- `LOCAL_ENGINE_KEY` – optional secret for local/testing access.

## Running Locally
Install dependencies and launch the FastAPI app using Uvicorn:

```bash
pip install fastapi uvicorn redis
uvicorn vault_engine.vault_api:app --reload
```

## Integration with the Sync Engine
The Sync engine queries the Vault to obtain connection health and build a user's integration map. This enables local prompts or re‑authentication flows whenever tokens expire or permissions change.

## Scaling & Resilience
- Multiple Vault instances can run behind a load balancer.
- The encrypted store can be backed by Redis, Dynamo or another scalable database.
- Logs are output in JSON and suitable for ingestion by Elastic, Loki or CloudWatch.
- Retrieval and refresh operations aim to complete in milliseconds to minimize latency for dependent engines.

## Insight Generation (Future)
While not currently enabled, the Vault can analyze logs to detect repeated OAuth failures and trends in token expiry. These insights can help surface reconnection prompts in the local UX.

## Testing
Run unit tests from the repository root:

```bash
pytest vault_engine/tests
```

