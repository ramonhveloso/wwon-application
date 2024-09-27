from typing import Optional

from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

    class Config:
        orm_mode = True
