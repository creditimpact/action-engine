# 🔐 Vault Engine – Secure Token Management for PURAIFI

**Vault Engine** is the centralized and secure storage service for all user-level credentials in the PURAIFI system.  
It acts as the digital "safe" that holds encrypted access tokens, user-platform connection statuses, and authorization metadata.  
Other engines (e.g., Action, Sync) rely on Vault to operate **on behalf of the user** — but without ever accessing raw credentials.

---

## 🧭 Role in the PURAIFI Ecosystem

Vault Engine ensures:
- 🔐 **Token security and storage** (OAuth access & refresh tokens)
- ✅ **Connection status management** per user and platform
- 🤝 **Centralized access control** – only engines can communicate with it
- 🧠 **Support for Sync Engine** in building integration maps

It does **not** interact with end-users directly.

---

## 🔁 Example Flows

### 1. Storing a new token
1. The local brain completes an OAuth flow (e.g. Google Calendar)
2. It sends a `POST /store_token` request:
   ```json
   {
     "user_id": "u123",
     "platform": "google_calendar",
     "token": {
       "access_token": "...",
       "refresh_token": "...",
       "expires_in": 3600,
       "scopes": ["calendar.read", "calendar.write"]
     }
   }
   ```
3. Vault:
   - Encrypts the token (AES-256)
   - Stores it under `user_id:platform`
   - Marks the platform as `active` for that user

### 2. Retrieving a token for an action
1. Action Engine sends a `POST /get_token` request:
   ```json
   {
     "user_id": "u123",
     "platform": "gmail"
   }
   ```
2. Vault checks:
   - Does the engine have permission?
   - Is the token valid (refresh if expired)?
   - If yes → returns token and expiry metadata

### 3. Sync Engine requests integration map
- Sends `GET /status?user_id=u123`
- Receives:
  ```json
  {
    "connected_platforms": [
      { "platform": "gmail", "status": "active" },
      { "platform": "notion", "status": "token_expired" },
      { "platform": "slack", "status": "not_connected" }
    ]
  }
  ```

---

## 🧱 Architecture

- **FastAPI**-based microservice
- **Stateless** – safe for load-balanced deployment
- Token store backed by **Redis** (or similar)
- Dual-layer **AES-256 encryption** for all secrets
- Request authentication via `X-Engine-ID` and `X-Engine-Key`
- Structured logging with UUID `request_id` for traceability

---

## 📦 Folder Structure

```
vault_engine/
├── vault_api.py              # REST API entry point
├── auth_middleware.py        # Validates engine identity
├── vault_storage.py          # Stores encrypted tokens (Redis or DB)
├── token_encryptor.py        # AES-256 encryption logic
├── token_refresher.py        # Refresh logic for expired tokens
├── connection_checker.py     # Platform connection status analyzer
├── vault_logger.py           # JSON logging for all operations
├── platform_profiles/        # YAML configs per platform
│   ├── google.yaml
│   ├── slack.yaml
│   └── notion.yaml
└── tests/
    └── test_token_flow.py
```

---

## ⚙️ API Endpoints

| Endpoint           | Method | Purpose                                     |
|--------------------|--------|---------------------------------------------|
| `/store_token`     | POST   | Store or update a token for a user          |
| `/get_token`       | POST   | Retrieve (and refresh if needed) a token    |
| `/status`          | GET    | Return connection statuses for a user       |

> All requests must include:
> - `X-Engine-ID: <engine_name>`  
> - `X-Engine-Key: <engine_secret>`

---

## 🔐 What Vault Stores

- Encrypted **OAuth access & refresh tokens**
- Platform-specific scopes (e.g., `calendar.write`, `mail.send`)
- Expiry metadata (for automatic refresh)
- Per-user connection state (`active`, `token_expired`, `missing`)
- Zero passwords – only tokenized credentials are handled

---

## 🔐 Security Model

Vault implements:
- ✅ **Zero Trust**: No request is trusted without authentication
- 🔐 **AES-256 encryption** of tokens + KMS-stored encryption keys
- 🔁 **Token refreshing** via platform-specific rules
- 📊 **Full audit logging** with `request_id`, engine, user, and outcome

---

## ⚡ Scalability & Resilience

- Stateless → can scale horizontally with multiple instances
- Redis/Dynamo/PostgreSQL support as backend store
- Logging is JSON-formatted → ready for ingestion by Loki, Elastic, CloudWatch
- Average token retrieval latency: **<10ms**

---

## 📊 Future Insight Capabilities

The Vault logs can be analyzed to surface insights such as:
- Common platform disconnections
- Token expiry trends
- OAuth failure rates by provider
- User segments with partial integrations

These insights can improve user onboarding and re-auth flows.

---

## 🔧 Configuration

Environment variables required:

| Variable                | Purpose                              |
|-------------------------|--------------------------------------|
| `VAULT_REDIS_URL`       | Redis or DB connection string        |
| `VAULT_ENCRYPTION_KEY`  | 32-byte key for AES-256 encryption   |
| `VAULT_ENCRYPTION_IV`   | 16-byte IV for AES                   |
| `ACTION_ENGINE_KEY`     | Shared secret for Action engine      |
| `SYNC_ENGINE_KEY`       | Shared secret for Sync engine        |
| `LOCAL_ENGINE_KEY`      | (Optional) Dev/test secret           |

---

## 🧪 Local Development

### Install dependencies:
```bash
pip install fastapi uvicorn redis
```

### Run the API server:
```bash
uvicorn vault_engine.vault_api:app --reload
```

### Run tests:
```bash
pytest vault_engine/tests
```

---

## 🧠 Summary

Vault Engine is the secure hub for all user tokens and permissions in PURAIFI.  
It guarantees that:
- Tokens are always encrypted and scoped per user
- Engines only access what they’re allowed to
- Re-auth flows are triggered when needed
- No user secret ever leaks across engine boundaries

It is modular, stateless, and built for scalable multi-engine coordination.

---
