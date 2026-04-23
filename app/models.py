from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str = ""


class Item(BaseModel):
    id: int
    name: str
    description: str = ""


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
