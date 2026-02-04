from sqlalchemy.orm import Session
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate

def get_items(db: Session):
    return db.query(Item).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item: ItemCreate):
    # 手動で1つずつ書くのではなく、model_dump() で一括変換します
    # これにより schemas/item.py で定義した status: "未完了" も反映されます
    db_item = Item(**item.model_dump()) 
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate):
    db_item = get_item(db, item_id)
    if db_item is None:
        return None
    
    # 送信された値だけをループで更新
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item is None:
        return False
    db.delete(db_item)
    db.commit()
    return True