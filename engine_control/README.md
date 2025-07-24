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

## 📦 Folder Structure (Example)

```
engine_control/
├── main.py                # FastAPI app entry point
├── auth_middleware.py     # Validates engine ID and token
├── permissions.py         # Permission model + enforcement logic
├── platform_status.py     # Tracks platform availability
├── config_manager.py      # Feature flags and API versions
├── logger.py              # JSON structured logger with request_id
├── engine_registry.py     # Manages engine registration and tokens
├── routes/                # API route handlers
│   ├── register.py
│   ├── check_permissions.py
│   ├── list_platforms.py
│   ├── config.py
│   └── log_event.py
└── tests/
    └── test_permissions.py
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
