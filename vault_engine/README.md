# Vault Engine

## 1. Introduction – What is the Vault?
PURAIFI Vault Engine is a dedicated microservice for securely managing OAuth credentials and platform profiles. It acts as the single source of truth for access and refresh tokens that other engines use when performing actions on a user's behalf. The service exposes only internal APIs—there are no user-facing endpoints—and every call is authenticated and logged. By isolating credential storage, the system enforces full Zero Trust principles and ensures that secrets never travel outside the vault without auditing.

## 2. Responsibilities & What It Stores
The vault keeps a per-user, per-platform record of:

- OAuth access and refresh tokens
- Expiration timestamps and granted scopes
- Encrypted keys derived from each user
- Status indicators for every platform (`connected`, `expired`, `missing`)
- Platform profile data (Google, Notion, Slack, etc.) used for refresh logic

Passwords are never stored; only the tokens issued by each platform are persisted.

## 3. Data Flow: How the Vault Works

### a. Store token
An engine sends token details along with the user and platform:

```json
{
  "user_id": "u1",
  "platform": "gmail",
  "access_token": "abcd",
  "refresh_token": "r1",
  "expires_at": 1700000000,
  "scopes": ["email"]
}
```
The vault encrypts and stores this under the key `u1:gmail` and marks Gmail as active for that user.

### b. Get token
When another engine needs a token it calls `/get_token` with the same identifiers. The vault validates the caller, checks expiry, and either returns the stored credentials or refreshes them first if possible.

### c. Get status
A status request returns a map of platforms for the user:

```json
{
  "connected_platforms": [
    { "platform": "Gmail", "status": "active" },
    { "platform": "Notion", "status": "missing" }
  ]
}
```

### d. Auto-refresh
If a retrieved token has expired and a refresh token is present, the vault performs a refresh before responding, storing the new data automatically.

## 4. Internal Architecture
| Module | Purpose |
| ------ | ------- |
| `vault_api.py` | REST API handlers |
| `auth_middleware.py` | Enforces engine authentication headers |
| `vault_storage.py` | Reads/writes encrypted tokens |
| `token_encryptor.py` | AES‑256 encryption/decryption helpers |
| `token_refresher.py` | Refresh logic for expired tokens |
| `connection_checker.py` | Reports connection health |
| `platform_profiles/` | YAML configs per supported platform |

Tokens are stored by key `<user_id>:<platform>`. Each token string is first encrypted with AES and then with a KMS‑managed key before being persisted to the backend store (Redis, DynamoDB, or PostgreSQL).

## 5. Security Model & Zero Trust
Only approved engines—`action`, `sync`, or `local`—may call the vault. Every request must include `X-Engine-ID` and `X-Engine-Key` headers which are checked by `auth_middleware.py`. All operations are logged with a request ID, user ID, platform, timestamp, action type, and result. Calls are specific to a given user and platform; generic token access is not possible.

## 6. Integration Map (for Sync Engine)
The sync engine queries the vault for the latest status of every platform a user has connected. The vault replies with a complete snapshot so Sync can determine which services need re‑authentication, which are ready for use, and which have never been connected. Vault provides raw status information while Sync interprets it and surfaces prompts to the user.

## 7. Error Handling & Resilience
Failures such as expired credentials, unauthorized engines, or storage errors return structured responses:

```json
{ "error_code": "expired_token", "message": "Token needs refresh", "suggested_action": "reauth" }
```
The vault retries transient storage issues and emits structured JSON logs (CloudWatch/Elastic ready) for monitoring.

## 8. Scaling & Performance
Vault Engine is a stateless FastAPI application that can scale horizontally behind a load balancer. Tokens reside in an encrypted database (Redis cluster, Dynamo, etc.) so any instance can handle requests. Token operations are cached and designed to be sub‑second. Logs are formatted for real‑time telemetry pipelines.

## 9. Running Locally (dev setup)
Install dependencies and start the service:

```bash
pip install fastapi uvicorn redis
uvicorn vault_engine.vault_api:app --reload
```

Run unit tests with:

```bash
pytest vault_engine/tests
```

## 10. Roadmap & Insights
Future extensions may include analytics over log data (e.g. "Google tokens often fail to refresh"), detecting partial user connection flows, and tighter integration with Sync Engine to proactively prompt users when credentials lapse.
