from app.models import Item

_store: dict[int, Item] = {}
_next_id: int = 1


def get_items() -> list[Item]:
    return list(_store.values())


def search_items_by_name(query: str) -> list[Item]:
    q = query.lower()
    return [item for item in _store.values() if q in item.name.lower()]


def get_item(item_id: int) -> Item | None:
    return _store.get(item_id)


def create_item(name: str, description: str = "") -> Item:
    global _next_id
    item = Item(id=_next_id, name=name, description=description)
    _store[_next_id] = item
    _next_id += 1
    return item


def update_item(item_id: int, name: str, description: str = "") -> Item | None:
    if item_id not in _store:
        return None
    item = Item(id=item_id, name=name, description=description)
    _store[item_id] = item
    return item


def delete_item(item_id: int) -> bool:
    if item_id not in _store:
        return False
    del _store[item_id]
    return True
