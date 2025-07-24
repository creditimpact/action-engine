# Action Engine

## 1. Introduction

The Action Engine is the execution layer of PURAIFI. It receives structured action templates from other services and carries out the requested operations against external platforms. It does not decide *what* to do—only *how* to do it once given a task. Typical actions include sending an email via Gmail, creating a Notion task or triggering a Zapier workflow. In the broader PURAIFI system, this engine acts as the bridge between high-level automation logic and concrete API calls.

## 2. How It Works – Flow Overview

1. A local system or orchestrator sends an action template to `/perform_action`.
2. The engine validates the caller's token using the Vault Engine.
3. The JSON payload is parsed into an internal `ActionModel`.
4. A matching adapter is chosen based on the target platform.
5. The adapter performs the external API call.
6. A standardized success or error result is returned.

Example request:

```json
{
  "user_id": "u1",
  "platform": "gmail",
  "action_type": "send_email",
  "payload": {"to": "user@example.com"}
}
```

Example response:

```json
{
  "status": "success",
  "result": {"message": "Email sent successfully"}
}
```

## 3. Architecture and Folder Structure

```
action_engine/
├─ main.py            – FastAPI application entry point
├─ router.py          – routes validated actions to adapters
├─ action_parser.py   – builds ActionModel objects
├─ executor.py        – helper for executing ActionModel instances
├─ adapters/          – platform specific integrations
├─ auth/              – JWT & OAuth helpers
├─ logging/           – request logging utilities
└─ tests/             – unit tests
```

`actions_registry.py` defines which actions are available per platform. The modular layout makes it easy to add new adapters or extend existing ones.

## 4. OAuth & Authentication

Authentication tokens are issued via `/login`. Some platforms require OAuth:

- `POST /auth/start` – begin the OAuth flow and receive an authorization URL.
- `POST /auth/callback` – handle the callback and store tokens securely in the Vault Engine.

Adapters fetch tokens from Vault as needed; no long‑term credentials are stored inside the service.

## 5. Supported Platforms & Actions

The registry currently includes:

- **gmail**: `send_email`
- **google_calendar**: `create_event`
- **notion**: `create_task`
- **zapier**: `trigger_zap`

Developers can extend the engine by adding new adapters and registering additional actions in `actions_registry.py`.

## 6. Error Handling & Monitoring

API errors, invalid input and token issues are caught and returned as structured JSON. Each request is logged with a `request_id`, `user_id` and timestamp. The engine never crashes on bad data—it always responds with either a success object or an error description.

## 7. Future Capabilities

Upcoming features include support for scheduled actions, conditional execution, multi‑step sequences and robust callbacks with retry logic.
