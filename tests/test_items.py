from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_item_returns_201():
    r = client.post("/items", json={"name": "widget", "description": "a test widget"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "widget"
    assert data["description"] == "a test widget"
    assert "id" in data


def test_list_items_empty_at_start():
    r = client.get("/items")
    assert r.status_code == 200
    assert r.json() == []


def test_list_items_returns_created():
    client.post("/items", json={"name": "alpha"})
    client.post("/items", json={"name": "beta"})
    r = client.get("/items")
    assert r.status_code == 200
    names = [i["name"] for i in r.json()]
    assert "alpha" in names
    assert "beta" in names


def test_get_item_by_id():
    created = client.post("/items", json={"name": "gadget"}).json()
    r = client.get(f"/items/{created['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "gadget"


def test_get_item_not_found():
    r = client.get("/items/99999")
    assert r.status_code == 404


def test_delete_item():
    created = client.post("/items", json={"name": "to-delete"}).json()
    r = client.delete(f"/items/{created['id']}")
    assert r.status_code == 204


def test_delete_item_not_found():
    r = client.delete("/items/99999")
    assert r.status_code == 404


def test_create_item_empty_name_rejected():
    r = client.post("/items", json={"name": "   ", "description": "test"})
    assert r.status_code == 422
