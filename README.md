# sandbox-fastapi-app

A monorepo sandbox used as a target for the **AI Dev Orchestrator**. It contains a minimal FastAPI CRUD service together with its models, in-memory storage layer, and test suite — all designed to be small enough to reason about quickly while still exercising realistic patterns.

---

## Repository layout

```
sandbox-fastapi-app/
├── main.py            # FastAPI application & route handlers
├── app/
│   ├── models.py      # Pydantic v2 request/response models
│   └── storage.py     # In-memory item store (no database)
├── tests/
│   └── test_items.py  # TestClient-based integration tests
├── requirements.txt   # Runtime dependencies
└── README.md          # This file
```

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Web framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Data validation | [Pydantic v2](https://docs.pydantic.dev/) |
| Server | [Uvicorn](https://www.uvicorn.org/) |
| Testing | [pytest](https://pytest.org/) + FastAPI `TestClient` |
| Storage | In-memory `dict` (no external database) |

---

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the development server (auto-reload on file changes)
uvicorn main:app --reload

# 3. Browse the interactive API docs
open http://127.0.0.1:8000/docs
```

### Running tests

```bash
pytest
```

---

## API reference

### Utility endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/ping` | Liveness check — returns `{"ping": "pong"}` |
| GET | `/version` | App metadata — returns `{"name": "Sandbox App", "version": "1.0.0"}` |
| GET | `/healthz` | Health check — returns `{"status": "ok", "version": "2.0", "environment": "sandbox"}` |

### Items CRUD

| Method | Path | Description |
|--------|------|-------------|
| GET | `/items` | List all items |
| GET | `/items/search?name={query}` | Search items by name (case-insensitive substring match) |
| GET | `/items/{id}` | Get a single item by ID |
| POST | `/items` | Create a new item (`name` required, `description` optional) |
| PATCH | `/items/{id}` | Partially update an item's `name` and/or `description` |
| DELETE | `/items/{id}` | Delete an item — returns `{"deleted": true, "id": <id>}` |

#### Item schema

```json
{
  "id": 1,
  "name": "widget",
  "description": "an optional description"
}
```

---

## Architecture notes

- **No database.** All item state lives in a module-level `dict` inside `app/storage.py`. The store is reset between test runs via a pytest `autouse` fixture.
- **Single process.** Because storage is in-memory, the app is intentionally single-process and not suitable for horizontal scaling without replacing the storage layer.
- **Flat route style.** Route handlers in `main.py` are thin; business logic (lookups, mutations) is delegated to `app/storage.py`.
- **AI Orchestrator target.** This repo exists to give the AI Dev Orchestrator a realistic but bounded codebase to practise code-generation, refactoring, and test-writing tasks against.
