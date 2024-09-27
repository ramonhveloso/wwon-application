from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.items.item_schemas import item as item_schema
from app.api.v1.items.item_service import item_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[item_schema.Item])
def get_items(db: Session = Depends(get_db)):
    return item_service.get_all_items(db)

@router.post("/", response_model=item_schema.Item)
def create_item(item: item_schema.ItemCreate, db: Session = Depends(get_db)):
    return item_service.create_item(db, item)
