import pytest
from app import storage


@pytest.fixture(autouse=True)
def reset_storage():
    storage._store.clear()
    storage._next_id = 1
    yield
