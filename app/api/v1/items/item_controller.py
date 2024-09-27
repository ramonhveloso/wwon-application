from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from app.api.v1.items.item_schemas import Item, ItemCreate
from app.api.v1.items.item_service import ItemService


router = APIRouter()

@router.get("/", response_model=list[Item])
def get_items(db: Session = Depends(get_db)):
    return ItemService.get_all_items(db)

@router.post("/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return ItemService.create_item(db, item)
