# Engine Control

Engine Control is the central coordination service for all engines in PURAIFI. It manages engine registration, platform availability and system policies rather than performing actions itself.

## Overview & Role

Engine Control acts as the meta-engine that governs what other engines may do. Engines authenticate to this service in order to register themselves, retrieve configuration, and check permissions before carrying out tasks on external platforms. The service is stateless and designed to run as a cloud API reachable by all engines but not by end users.

Main responsibilities include:

- Registering and validating engines
- Controlling the list of supported platforms and their statuses
- Checking whether an action is allowed for a particular engine
- Storing global feature flags and API versions
- Logging engine activity for auditing purposes

## System Context

Engine Control runs as a standalone HTTP service. Other engines such as the Action Engine or Vault Engine query it via REST or gRPC to verify whether they are allowed to perform a given operation. No engine is implicitly trusted; each request requires the caller to present its engine ID and secret key.

## Core API Endpoints

The service exposes several endpoints to handle registration, permission checks and configuration. Example routes are shown below.

| Endpoint | Method | Description |
| --- | --- | --- |
| `/engines/register` | `POST` | Register a new engine and define its permissions and dependencies. Returns a token used for future calls. |
| `/engines/validate` | `POST` | Validate an engine's identity using its token. Used by engines to confirm they are recognised. |
| `/actions/check` | `POST` | Determine whether a given engine can perform an action on a platform. Also returns any required scopes. |
| `/platforms/list` | `GET` | List available platforms with their current status (`active`, `maintenance`, `deprecated`). |
| `/config/global` | `GET` | Fetch global feature flags and API version information. |
| `/log/engine_event` | `POST` | Submit event logs such as errors or metrics for aggregation. |

### Example flow: registering an engine

1. A new engine sends a `POST /engines/register` request with its desired permissions.
2. Engine Control stores the engine entry and returns a unique authentication token.
3. The engine uses this token for subsequent calls via the `X-Engine-ID` and `X-Engine-Key` headers.

### Example flow: requesting permission for an action

1. Before performing an action, the engine calls `POST /actions/check` with its engine ID, the target platform and the action type.
2. Engine Control verifies the engine's registration, platform status and permission set.
3. A response is returned indicating whether the action is allowed and which scopes are required.

### Handling platform maintenance

When a platform is put into maintenance mode via configuration, `POST /platforms/list` will show its status as `maintenance`. Permission checks for that platform will fail until the status is restored to `active`.

## Permission & Policy Model

Each engine is registered with a set of allowed platforms and actions. The service enforces these policies on every permission check. Dynamic feature flags can temporarily enable or disable platforms or specific use cases without requiring code changes.

## Security Model

Engine Control follows a zero-trust approach:

- Requests must include a valid engine ID and token.
- Permissions are checked for every action; lack of permission results in denial.
- All operations are logged with request IDs to provide a full audit trail.

There is no implicit trust between engines. Even internal calls are authenticated and logged.

## Scalability & Extensibility

The API is stateless and suitable for horizontal scaling behind a load balancer. Engines can be onboarded dynamically by calling the registration endpoint, and platform statuses can be updated without redeploying. Responses are version-aware so that outdated clients can be warned when new features become available.

## Internal Logic

While the public API focuses on configuration and authorization, internally the service maintains in‑memory stores for engines and platform status. Each request goes through an authentication middleware that validates the `X-Engine-ID` and `X-Engine-Key` headers. Permission checks combine the engine's stored permissions with the platform status to decide whether an action is allowed. All endpoints use a JSON logger that attaches a per‑request UUID for traceability.

## Sample Development Setup

1. Install requirements:

   ```bash
   pip install fastapi uvicorn
   ```

2. Start the service:

   ```bash
   uvicorn engine_control.main:app --reload
   ```

Other engines can then send HTTP requests to this local instance. Tests can be run with `pytest` from the repository root.

