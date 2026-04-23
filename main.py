from fastapi import FastAPI, HTTPException
from app.models import Item, ItemCreate, ItemUpdate
from app.storage import get_items, get_item, create_item, delete_item, update_item, search_items_by_name

app = FastAPI(title="Sandbox App", version="1.0.0")


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/items", response_model=list[Item])
def list_items():
    return get_items()


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=Item, status_code=201)
def create(payload: ItemCreate):
    if not payload.name or not payload.name.strip():
        raise HTTPException(status_code=422, detail="Item name must not be empty")
    return create_item(payload.name, payload.description)


@app.patch("/items/{item_id}", response_model=Item)
def update(item_id: int, payload: ItemUpdate):
    existing = get_item(item_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Item not found")
    new_name = payload.name if payload.name is not None else existing.name
    new_description = payload.description if payload.description is not None else existing.description
    return update_item(item_id, new_name, new_description)


@app.delete("/items/{item_id}", status_code=204)
def delete(item_id: int):
    if not delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
