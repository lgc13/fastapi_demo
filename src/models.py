from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Item(SQLModel, table=True):
    id: int = Field(primary_key=True)
    text: str
    is_complete: bool


class ItemRequest(BaseModel):
    text: str


class ItemPatchRequest(BaseModel):
    is_complete: bool


print(">>>> IN models.py")
