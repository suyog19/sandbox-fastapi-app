from pydantic import BaseModel, field_validator


class ItemCreate(BaseModel):
    name: str
    description: str = ""

    @field_validator("description")
    @classmethod
    def description_must_not_be_blank(cls, v: str) -> str:
        if v != "" and not v.strip():
            raise ValueError("description must not be an empty or whitespace-only string")
        return v


class Item(BaseModel):
    id: int
    name: str
    description: str = ""

    @field_validator("description")
    @classmethod
    def description_must_not_be_blank(cls, v: str) -> str:
        if v != "" and not v.strip():
            raise ValueError("description must not be an empty or whitespace-only string")
        return v
