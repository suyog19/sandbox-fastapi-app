import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

def test_create_item_returns_201():
    r = client.post("/items", json={"name": "widget", "description": "a test widget"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "widget"
    assert data["description"] == "a test widget"
    assert "id" in data


def test_create_item_no_description():
    r = client.post("/items", json={"name": "minimal"})
    assert r.status_code == 201
    assert r.json()["description"] == ""


def test_create_item_empty_name_rejected():
    r = client.post("/items", json={"name": "   ", "description": "test"})
    assert r.status_code == 422


def test_create_item_missing_name_rejected():
    r = client.post("/items", json={"description": "no name"})
    assert r.status_code == 422


def test_create_item_ids_are_unique():
    a = client.post("/items", json={"name": "a"}).json()
    b = client.post("/items", json={"name": "b"}).json()
    assert a["id"] != b["id"]


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------

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


def test_list_items_count():
    client.post("/items", json={"name": "x1"})
    client.post("/items", json={"name": "x2"})
    client.post("/items", json={"name": "x3"})
    assert len(client.get("/items").json()) == 3


# ---------------------------------------------------------------------------
# Get by ID
# ---------------------------------------------------------------------------

def test_get_item_by_id():
    created = client.post("/items", json={"name": "gadget"}).json()
    r = client.get(f"/items/{created['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "gadget"


def test_get_item_not_found():
    r = client.get("/items/99999")
    assert r.status_code == 404


def test_get_item_returns_correct_fields():
    created = client.post("/items", json={"name": "probe", "description": "checking fields"}).json()
    fetched = client.get(f"/items/{created['id']}").json()
    assert fetched["id"] == created["id"]
    assert fetched["name"] == "probe"
    assert fetched["description"] == "checking fields"


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

def test_delete_item():
    created = client.post("/items", json={"name": "to-delete"}).json()
    r = client.delete(f"/items/{created['id']}")
    assert r.status_code == 204


def test_delete_removes_item():
    created = client.post("/items", json={"name": "gone"}).json()
    client.delete(f"/items/{created['id']}")
    assert client.get(f"/items/{created['id']}").status_code == 404


def test_delete_removes_from_list():
    created = client.post("/items", json={"name": "listed-then-gone"}).json()
    client.delete(f"/items/{created['id']}")
    ids = [i["id"] for i in client.get("/items").json()]
    assert created["id"] not in ids


def test_delete_item_not_found():
    r = client.delete("/items/99999")
    assert r.status_code == 404


def test_double_delete_returns_404():
    created = client.post("/items", json={"name": "double-delete"}).json()
    client.delete(f"/items/{created['id']}")
    assert client.delete(f"/items/{created['id']}").status_code == 404


# ---------------------------------------------------------------------------
# Future features — skip-marked so they appear in pytest output as targets
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="planned: PATCH /items/{id} not yet implemented")
def test_update_item_name():
    created = client.post("/items", json={"name": "old-name"}).json()
    r = client.patch(f"/items/{created['id']}", json={"name": "new-name"})
    assert r.status_code == 200
    assert r.json()["name"] == "new-name"


@pytest.mark.skip(reason="planned: PATCH /items/{id} not yet implemented")
def test_update_item_description_only():
    created = client.post("/items", json={"name": "keep-name", "description": "old"}).json()
    r = client.patch(f"/items/{created['id']}", json={"description": "new"})
    assert r.status_code == 200
    assert r.json()["name"] == "keep-name"
    assert r.json()["description"] == "new"


@pytest.mark.skip(reason="planned: GET /items?search= not yet implemented")
def test_search_items_by_name():
    client.post("/items", json={"name": "searchable-item"})
    r = client.get("/items", params={"search": "searchable"})
    assert r.status_code == 200
    assert any("searchable" in i["name"] for i in r.json())


@pytest.mark.skip(reason="planned: GET /items?page=&limit= pagination not yet implemented")
def test_pagination_returns_correct_page():
    for i in range(5):
        client.post("/items", json={"name": f"page-item-{i}"})
    r = client.get("/items", params={"page": 1, "limit": 2})
    assert r.status_code == 200
    assert len(r.json()) == 2
