# sandbox-fastapi-app

A minimal FastAPI app used as a sandbox target for the AI Dev Orchestrator.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/ping` | Liveness check — returns `{"ping":"pong"}` |
| GET | `/version` | App version — returns `{"name":"Sandbox App","version":"1.0.0"}` |
| GET | `/healthz` | Health check — returns `{"status":"ok","version":"2.0","environment":"sandbox"}` |
| GET | `/items` | List all items |
| GET | `/items/search?name={query}` | Search items by name |
| GET | `/items/{id}` | Get item by ID |
| POST | `/items` | Create item |
| DELETE | `/items/{id}` | Delete item — returns 200 `{"deleted":true,"id":<id>}` |
