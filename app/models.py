from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(default="", max_length=500)


class Item(BaseModel):
    id: int
    name: str = Field(..., max_length=100)
    description: str = Field(default="", max_length=500)
