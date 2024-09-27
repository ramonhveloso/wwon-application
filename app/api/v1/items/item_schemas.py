from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str

class Item(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
