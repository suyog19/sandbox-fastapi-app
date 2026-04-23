from app.models import Item

_store: dict[int, Item] = {}
_next_id: int = 1


def get_items() -> list[Item]:
    return list(_store.values())


def get_item(item_id: int) -> Item | None:
    return _store.get(item_id)


def create_item(name: str, description: str = "") -> Item:
    global _next_id
    item = Item(id=_next_id, name=name, description=description)
    _store[_next_id] = item
    _next_id += 1
    return item


def delete_item(item_id: int) -> bool:
    if item_id not in _store:
        return False
    del _store[item_id]
    return True
