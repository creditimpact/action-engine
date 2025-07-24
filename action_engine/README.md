# Action Engine

The **action_engine** is the execution layer of PURAIFI. It acts as the system's
"hands" and is responsible for carrying out concrete operations such as sending
emails, creating calendar events, creating tasks and triggering external
integrations.

This README describes how the engine fits into the wider system, the supported
actions in the first version and how the code is structured so that developers
can extend it.

## Overview & Purpose

At runtime the orchestrator (or the local core during development) sends
structured action templates to the action engine. The engine validates those
actions, fetches any required OAuth tokens from the Vault Engine and executes
them using platform specific adapters. Permission checks are delegated to the
Engine Control service which determines whether the requesting engine is allowed
to perform the requested action.

The action engine itself does not store any user data long term; it only
retrieves the minimal credentials required to execute an action and discards any
intermediate state once the call has completed.

## System Integration

1. **Input** – The orchestrator/local core issues a JSON action template and
   sends it to the `/perform_action` endpoint.
2. **Validation** – The payload is validated by `validator.py` to ensure all
   required fields are present.
3. **Action Model** – `action_parser.py` converts the validated data into an
   `ActionModel` object which flows through the engine.
4. **Permission Check** – Before executing, Engine Control may be queried to
   verify that the action is allowed for the calling engine and that the target
   platform is currently available.
5. **Token Retrieval** – The adapter obtains OAuth credentials from the Vault
   Engine via the `token_manager` module. Tokens are stored encrypted in Redis
   and are refreshed on demand.
6. **Execution** – The appropriate adapter issues an external API call.
7. **Response** – Results are returned in a standard JSON structure for the
   orchestrator to consume.

## Supported Action Types (v1)

The initial registry of supported platforms and actions resides in
`actions_registry.py`:

- `gmail`: `send_email`, `perform_action`
- `google_calendar`: `create_event`
- `notion`: `create_task`
- `zapier`: `trigger_zap`, `perform_action`

Adapters may implement additional helper methods. Any function listed in the
registry can be invoked through `/perform_action`.

## Internal Architecture

```
action_engine/
├─ main.py            – FastAPI application and HTTP endpoints
├─ router.py          – routes validated actions to adapters
├─ validator.py       – request validation
├─ action_parser.py   – builds ActionModel objects
├─ executor.py        – helper for executing ActionModel instances
├─ adapters/          – platform specific integrations
├─ auth/              – JWT handling and OAuth token storage
├─ logging/           – JSON logger and request ID middleware
└─ actions_registry.py – list of allowed actions per platform
```

### The `ActionModel`

```python
@dataclass
class ActionModel:
    action_type: str
    platform: str
    user_id: str
    payload: Dict[str, Any]
```

An `ActionModel` represents a single unit of work. After validation, incoming
requests are converted into this object so that the internal code works with a
consistent structure regardless of the external representation.

## Flow Diagram / Lifecycle

1. **HTTP Request** – `/perform_action` receives JSON with `user_id`,
   `platform`, `action_type` and `payload`.
2. **Validation** – `validator.validate_request` ensures all fields exist;
   otherwise an HTTP 400 error is returned.
3. **Parsing** – `action_parser.parse_request` produces an `ActionModel`.
4. **Routing** – `router.route_action` selects the adapter for the platform and
   invokes the method matching `action_type`.
5. **Token Handling** – The adapter calls `token_manager.get_access_token`, which
   interacts with the Vault Engine. If the token has expired it is refreshed via
   its refresh token.
6. **External Call** – The adapter performs the API request (e.g. Gmail, Google
   Calendar, Notion, Zapier). HTTP helpers in `BaseAdapter` handle errors and
   token injection.
7. **Response Formatting** – Adapters return a dictionary describing the result.
   The router wraps this dictionary in `{"status": "success", "result": ...}` or
   standardised error structures on failure.

## Extensibility

New platforms can be added by creating a module under `adapters/` that extends
`BaseAdapter` and by registering supported action names in
`actions_registry.py`. Each adapter is responsible for translating generic
payloads into provider specific API calls.

Additional validation logic can be placed in `validator.py` or in the adapter
itself using pydantic models. Because actions are looked up dynamically via the
registry, adding a new action usually only requires implementing a new adapter
method and updating the registry.

## Error Handling & Observability

- Adapters raise `HTTPException` for validation or API errors. The router
  catches these and returns structured responses:

  ```json
  {
    "error": "Missing token for gmail"
  }
  ```

- Every request is tagged with a UUID request ID via `RequestIdMiddleware` and
  all logs are emitted in JSON format by `logging/logger.py`. Sensitive values
  such as tokens are filtered out.
- The engine can retry or fall back at the orchestrator level if an adapter
  indicates failure. External failures do not persist any partial state.

## Security Considerations

- OAuth tokens are managed by the Vault Engine. They are encrypted in Redis and
  only decrypted when requested by an adapter. The action engine never stores
  plaintext tokens on disk.
- Payloads are kept in memory only for the duration of a single request. No
  long‑term user data is persisted by the engine itself.
- JWTs are used to authenticate calls to `/perform_action` and to the OAuth
  helper endpoints.

## Examples

### Send an email via Gmail

**Request**

```json
{
  "user_id": "u1",
  "platform": "gmail",
  "action_type": "send_email",
  "payload": {"to": "test@example.com"}
}
```

**Response**

```json
{
  "status": "success",
  "result": {
    "status": "success",
    "platform": "gmail",
    "message": "Email sent successfully",
    "data": {"to": "test@example.com"}
  }
}
```

### Create a calendar event

```json
{
  "user_id": "u1",
  "platform": "google_calendar",
  "action_type": "create_event",
  "payload": {"title": "Project Kickoff"}
}
```

Response:

```json
{
  "status": "success",
  "result": {
    "status": "success",
    "platform": "google_calendar",
    "message": "\u05d0\u05d9\u05e8\u05d5\u05e2 \u05e0\u05d5\u05e6\u05e8 \u05d1\u05d4\u05e6\u05dc\u05d7\u05d4",
    "data": {"title": "Project Kickoff"}
  }
}
```

### Adapter implementation snippet

```python
class GmailAdapter(BaseAdapter):
    SEND_API_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"

    async def send_email(self, user_id: str, payload: dict) -> dict:
        _validate(payload, GmailSendEmailPayload)
        token = await self._get_token(user_id)
        await self.post(
            self.SEND_API_URL,
            headers={"Authorization": f"Bearer {token}"},
            data=payload,
        )
        return {
            "status": "success",
            "platform": "gmail",
            "message": "Email sent successfully",
            "data": payload,
        }
```

## Running Locally

Install dependencies and start the service with Uvicorn:

```bash
pip install fastapi uvicorn
uvicorn action_engine.main:app --reload
```

Use `/login` to obtain a JWT for a user and include it in the
`Authorization` header when calling `/perform_action` or the OAuth helper
endpoints.

