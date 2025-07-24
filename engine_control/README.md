# Engine Control

## 1. Introduction: What is Engine Control?
Engine Control is the meta-engine that governs every other engine in the PURAIFI ecosystem. It does not execute tasks itself. Instead it registers engines, enforces permissions, manages platform availability and serves global configuration. By centralizing these checks it ensures that only authorised engines can interact with external services. End users never call this API directly—only engines communicate with it.

## 2. Permission Model
Engine Control follows a strict zero-trust approach:
- Each engine registers with an `engine_id` and receives a signed `engine_token`.
- Every action request is validated against the stored permissions; there are no default allowances.
- Platform status (for example `maintenance`) can override individual engine permissions.
- Engines may depend on other engines. If a dependency is inactive, related actions are denied.

## 3. Core API Endpoints
| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/engines/register` | `POST` | Register a new engine and obtain a token |
| `/engines/validate` | `POST` | Confirm engine identity |
| `/actions/check` | `POST` | Ask if a proposed action is allowed |
| `/platforms/list` | `GET` | Get platform statuses and available scopes |
| `/config/global` | `GET` | Retrieve system-wide flags, versions and modes |
| `/log/engine_event` | `POST` | Submit telemetry or logs from engines |

**Request example:**
```json
POST /engines/register
{
  "engine_id": "sync",
  "permissions": {"gmail": {"read": ["gmail.read"]}}
}
```
**Response example:**
```json
{
  "engine_token": "<signed-token>"
}
```

## 4. Typical Flows
### Registering a new engine
Send a `POST /engines/register` request with the desired permissions and dependencies. The response contains an `engine_token` used in future requests.

### Performing an action
Before calling another engine such as Vault, the caller must check its rights via `POST /actions/check`.
If the platform is in maintenance or the scope is missing, the response will deny the action with a reason.

### Getting global config
Engines periodically call `GET /config/global` to retrieve feature flags or version information that might alter their behaviour.

## 5. Internal Model (What Engine Control stores)
For every engine the service records:
- `engine_id`, `name` and a `token`
- Allowed platforms and actions
- Optional `depends_on` list

Platform status is tracked globally and consulted during every permission check.

## 6. Logging, Monitoring & Deactivation
Every request receives a unique `request_id` and is logged with fields such as `engine_id`, `action`, `platform`, result and timestamp. Engines can be flagged as inactive; once flagged, all calls from them are rejected. Alerts can trigger if repeated failures or suspicious behaviour is detected.

## 7. Scalability & Extensibility
The API is stateless which allows horizontal scaling. New engines or platforms can be added without code changes because permissions and platform status are stored dynamically. Feature flags and version-aware responses enable gradual rollout and warnings when an engine is outdated.

## 8. Development Setup
```bash
pip install fastapi uvicorn
uvicorn engine_control.main:app --reload
```
