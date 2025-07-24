# Action Engine

Action Engine is a lightweight FastAPI service for routing automation requests to various platforms. Requests are parsed and forwarded to platform specific adapters located in `action_engine/adapters`.

## Folder structure

- `action_engine/main.py` – FastAPI application entry point.
- `action_engine/router.py` – routes requests to the correct adapter.
- `action_engine/adapters/` – adapters for external platforms such as Gmail, Notion, Google Calendar and Zapier.
- `action_engine/actions_registry.py` – registry describing available actions per platform.
- Other directories (`auth`, `logging`, `tests`, `utils`) contain placeholder modules for future extensions.

## Running the app

1. Install dependencies (for example with pip):

   ```bash
   pip install fastapi uvicorn
   ```

2. Start the FastAPI server with Uvicorn from the repository root:

   ```bash
   uvicorn action_engine.main:app --reload
   ```

The API exposes a `/perform_action` endpoint that accepts a JSON payload with `platform`, `action_type` and `payload` fields.

## Supported platforms and actions

The currently registered platforms and actions are defined in `actions_registry.py`:

- **gmail**: `perform_action`
- **google_calendar**: `create_event`
- **notion**: `create_task`
- **zapier**: `perform_action`

Additional adapter functions (e.g. `send_email` in the Gmail adapter) can be used by calling the relevant function names via the API.

## Initiating OAuth

Some adapters require OAuth tokens. Use the `/auth/start` and `/auth/callback` endpoints to complete the flow:

1. **Start authorization**

   ```bash
   curl -X POST http://localhost:8000/auth/start \
        -H "X-API-Key: <your key>" \
        -d '{"user_id": "u1", "platform": "gmail", "client_id": "id", "client_secret": "secret", "redirect_uri": "https://app/callback"}'
   ```

   The response contains `authorization_url` that the user should visit.

2. **Handle the callback**

   After the user authorizes the application, POST the received information to `/auth/callback`:

   ```bash
   curl -X POST http://localhost:8000/auth/callback \
        -H "X-API-Key: <your key>" \
        -d '{"user_id": "u1", "platform": "gmail", "client_id": "id", "client_secret": "secret", "redirect_uri": "https://app/callback", "authorization_response": "..."}'
   ```

   On success the access and refresh tokens are stored and can be retrieved by the adapters when performing actions.
