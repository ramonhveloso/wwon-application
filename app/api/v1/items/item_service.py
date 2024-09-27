from sqlalchemy.orm import Session
from app.api.v1.items.item_schemas import item as item_schema
from app.db.models.item import Item

def create_item(db: Session, item: item_schema.ItemCreate):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_items(db: Session):
    return db.query(Item).all()
