import uuid
from app.models import Item

_store: dict[str, Item] = {}


def get_items() -> list[Item]:
    return list(_store.values())


def get_item(item_id: str) -> Item | None:
    return _store.get(item_id)


def create_item(name: str, description: str = "") -> Item:
    item_id = str(uuid.uuid4())
    item = Item(id=item_id, name=name, description=description)
    _store[item_id] = item
    return item


def delete_item(item_id: str) -> bool:
    if item_id not in _store:
        return False
    del _store[item_id]
    return True
