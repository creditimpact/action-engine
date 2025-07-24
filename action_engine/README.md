# 🧠 Action Engine – PURAIFI Execution Service

**Action Engine** is the execution arm of the PURAIFI system.  
It receives structured action requests from the local brain and performs digital operations such as sending emails, creating calendar events, triggering Zaps, or opening tasks in Notion.

This engine **does not decide** what to do — it **only executes** pre-defined instructions passed to it in a consistent template format.  
Its role is to interface with external APIs securely and reliably, abstracting away token management, action formatting, and error handling.

---

## 🧭 Role in the System

Action Engine is one of several modular services in the PURAIFI platform. It works in coordination with:

- 🔐 **Vault Engine** – provides access tokens securely per user and per platform.
- 🧠 **Local Brain** – sends execution requests with `user_id`, `platform`, `action_type`, and structured `payload`.
- ⚙️ **Engine Control** – validates whether an engine is allowed to perform a given action.

This separation of concerns ensures:
- Clear boundaries between decision-making and execution
- Token safety (Action never sees passwords or unencrypted tokens)
- Scalable multi-platform integrations

---

## 🚀 How It Works – Flow Overview

### 1. The local system generates an action:
```json
{
  "platform": "gmail",
  "action_type": "send_email",
  "payload": {
    "to": "user@example.com",
    "subject": "Hello!",
    "body": "How are you?"
  }
}
```

### 2. Action Engine:
- Parses the request
- Validates permissions and token access
- Selects the appropriate **adapter** for the platform
- Calls the external API
- Returns a unified response (success or error)

### 3. Sample response:
```json
{
  "status": "success",
  "platform": "gmail",
  "action_type": "send_email",
  "result": {
    "message_id": "abc123",
    "timestamp": "2025-07-25T15:21:00Z"
  }
}
```

---

## 📦 Folder Structure

```
action_engine/
├── main.py                # FastAPI app entry point
├── router.py              # HTTP route handlers
├── action_parser.py       # Parses incoming requests
├── actions_registry.py    # Maps platform + action to adapter
├── executor.py            # Executes formatted actions
├── formatter.py           # Creates platform payloads
├── validator.py           # Request validation logic
├── config.py              # Engine configuration
├── .env.example           # Sample environment variables
├── .env                   # Local overrides
├── adapters/              # Platform integrations
│   ├── gmail_adapter.py
│   ├── google_calendar_adapter.py
│   ├── notion_adapter.py
│   └── zapier_adapter.py
├── auth/                  # OAuth and token utilities
│   ├── jwt_manager.py
│   ├── oauth_client.py
│   └── token_manager.py
├── logging/               # Structured logging
│   └── logger.py
├── utils/                 # Helper functions
│   └── common.py
├── tests/                 # Unit tests
│   ├── conftest.py
│   ├── test_adapters.py
│   ├── test_auth.py
│   ├── test_logging.py
│   ├── test_oauth.py
│   ├── test_router.py
│   ├── test_router_concurrent.py
│   └── test_token_manager.py
```

---

## ✅ Supported Platforms and Actions

All available actions are listed in `actions_registry.py`.

| Platform         | Action Types      |
|------------------|-------------------|
| `gmail`          | `send_email`      |
| `google_calendar`| `create_event`    |
| `notion`         | `create_task`     |
| `zapier`         | `trigger_zap`     |

> You can extend this engine by adding a new adapter and registering its functions in `actions_registry.py`.

---

## 🔐 OAuth and Authentication

Some platforms require user-level OAuth tokens. These are stored and retrieved securely from the **Vault Engine**.

### OAuth Flow (via local or frontend):
1. Call `/auth/start` with platform + redirect info → receive `authorization_url`
2. User logs in and authorizes
3. Callback sent to `/auth/callback` → token is securely saved

Tokens are **never stored** in the Action Engine — they're pulled from Vault when needed.

---

## ⚙️ API Endpoints

| Method & Path         | Purpose                        |
|------------------------|--------------------------------|
| `POST /perform_action` | Execute an action on a platform |
| `POST /auth/start`     | Begin OAuth flow for a platform |
| `POST /auth/callback`  | Complete OAuth and store token |
| `POST /login`          | Get a dev/test token (optional) |

> All endpoints require a Bearer token (e.g., `Authorization: Bearer <token>`)

---

## 🧪 Running Locally

```bash
pip install fastapi uvicorn
uvicorn action_engine.main:app --reload
```

Use tools like Postman or `curl` to call endpoints during development.

---

## 📈 Logging and Monitoring

Each request is assigned a `request_id` and logged in structured JSON format.  
Logs include:

- `user_id`
- `platform`
- `action_type`
- `status`: `success` or `error`
- `timestamp`

This enables cross-engine tracing and system-wide observability.

---

## 🧩 Future Features

- Multi-step action sequences
- Conditional execution
- Delayed / scheduled actions
- Support for multi-user workflows

---

## 🧠 Summary

Action Engine:
- Executes digital actions securely
- Interfaces with Gmail, Notion, Zapier, etc.
- Delegates token management to Vault
- Works under control of the system’s central brain

It is stateless, modular, and built for scalable execution across diverse platforms.

---
