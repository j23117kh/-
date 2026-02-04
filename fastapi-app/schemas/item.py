from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

# 共通フィールド
class ItemBase(BaseModel):
    subject: str
    title: str
    due_date: date
    priority: str

# 作成時
class ItemCreate(ItemBase):
    pass

# 更新時 (全ての項目を任意に)
class ItemUpdate(BaseModel):
    subject: Optional[str] = None
    title: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None

# 応答用
class ItemResponse(ItemBase):
    id: int
    status: str
    
    model_config = ConfigDict(from_attributes=True)