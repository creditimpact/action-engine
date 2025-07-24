# 🧠 Engine Control – Central Coordination Service for PURAIFI

**Engine Control** is the central orchestrator in the PURAIFI system.  
It governs **which engines may perform which actions**, enforces platform-level policies, and logs system-wide activity.  
This service does **not perform any direct actions** – it acts as the policy gatekeeper for all execution engines.

---

## 🧭 Role in the PURAIFI System

Engine Control serves as the meta-engine that ensures order and safety across the system.

It handles:
- 🔐 **Engine authentication and registration**
- ✅ **Permission checks** for every action attempt
- 📡 **Platform availability and version flags**
- 📊 **Logging and observability for auditing and metrics**

> No engine is implicitly trusted. Each action must be explicitly authorized.

---

## 🔁 Common Flows

### 🔧 Engine Registration Flow

1. New engine calls `POST /engines/register` with its desired capabilities.
2. Engine Control returns an engine token (secret key).
3. The engine includes this token in `X-Engine-ID` and `X-Engine-Key` headers on every future request.

### ✅ Permission Check Flow

1. Engine wants to execute an action (e.g., send email).
2. It calls `POST /actions/check` with:
   ```json
   {
     "engine_id": "action",
     "platform": "gmail",
     "action_type": "send_email"
   }
   ```
3. Engine Control responds:
   ```json
   {
     "allowed": true,
     "required_scopes": ["mail.send"]
   }
   ```

If the platform is under maintenance or the engine lacks permission → `allowed: false`.

---

## 📦 Folder Structure

```
engine_control/
├── main.py                # FastAPI app entry point
├── engine_api.py          # HTTP route handlers
├── engine_config.py       # Engine configuration
├── engine_registry.py     # Tracks registered engines
├── permission_checker.py  # Authorization logic
├── platform_registry.py   # Supported platforms list
├── platform_config.py     # Platform settings
├── auth_middleware.py     # Validates engine identity
├── engine_logger.py       # Structured logging
├── config.py              # Service configuration
├── .env.example           # Sample environment variables
├── .env                   # Local overrides
├── schemas/               # Pydantic models
│   ├── engine.py
│   └── platform.py
├── store/                 # In-memory data stores
│   ├── engine_store.py
│   └── platform_store.py
├── tests/                 # Unit tests
│   ├── conftest.py
│   ├── test_action_check.py
│   ├── test_authorization.py
│   ├── test_engine_register.py
│   └── test_platforms_list.py
```

---

## ⚙️ API Endpoints

| Endpoint               | Method | Purpose                                           |
|------------------------|--------|---------------------------------------------------|
| `/engines/register`    | POST   | Register a new engine with its permissions        |
| `/engines/validate`    | POST   | Verify an engine’s identity using token           |
| `/actions/check`       | POST   | Check if an engine is allowed to perform an action|
| `/platforms/list`      | GET    | View available platforms and their statuses       |
| `/config/global`       | GET    | Get feature flags and API version info            |
| `/log/engine_event`    | POST   | Submit logs or events for central collection      |

> All requests require headers:  
> `X-Engine-ID: <engine_name>`  
> `X-Engine-Key: <engine_secret>`

---

## 🔐 Permission & Policy Model

Each engine has:
- Allowed platforms (e.g. Gmail, Slack)
- Allowed actions per platform (e.g. `send_email`, `create_event`)
- Dynamic feature flags that enable/disable actions without redeploying

Every `check` request verifies:
- The engine’s identity (auth)
- Whether the action is in its permission set
- Whether the platform is available (e.g. not in `maintenance` mode)

---

## 🛡️ Security Model

Engine Control enforces a **Zero Trust** architecture:

- No engine is trusted by default
- Tokens are required and validated on each request
- Permissions are re-evaluated for every action
- Logs are recorded for traceability (with `request_id`, engine, action, result)

Even internal calls between engines are **authenticated and logged**.

---

## 📈 Scalability & Reliability

- Fully stateless – can run behind a load balancer
- In-memory cache for quick access to engine and platform data
- Real-time updates to platform status and config without restart
- Versioned API responses for future-proof compatibility

---

## 🧪 Local Development

### Install dependencies:
```bash
pip install fastapi uvicorn
```

### Run the service:
```bash
uvicorn engine_control.main:app --reload
```

Other engines can now make HTTP requests to `localhost:8000`.  
Run tests with:

```bash
pytest engine_control/tests
```

---

## 📊 Logging & Observability

Each API call is logged in structured JSON format with:

- `request_id`
- `engine_id`
- `platform`
- `action_type`
- `status`: allowed / denied / error
- `timestamp`

These logs enable full auditability and system-level behavior tracking.

---

## 🧠 Summary

Engine Control is:
- The **policy brain** of PURAIFI’s distributed engine system
- Responsible for verifying, gating and auditing all external actions
- A central hub for platform status, API governance and feature flags

It ensures PURAIFI can scale safely while retaining fine-grained control over every action.

---
