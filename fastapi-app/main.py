from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# 1. データベース基盤のインポート
from db import Base, engine, get_db
# 2. モデルを必ず先にインポート（これでBaseがテーブルを認識する）
import models.item 
# 3. その他の部品をインポート
from schemas.item import ItemCreate, ItemUpdate, ItemResponse
from crud.item import get_items, get_item, create_item, update_item, delete_item

# --- アプリ起動時にテーブルを強制作成 ---
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS設定：あらゆる接続元を一時的に許可して疎通を優先
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)

@app.post("/items", response_model=ItemResponse)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item_endpoint(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    updated = update_item(db, item_id, item)
    if updated is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@app.delete("/items/{item_id}")
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    if not delete_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"result": "ok"}