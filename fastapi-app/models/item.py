from sqlalchemy import Column, Integer, String, Date
from db import Base 

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    title = Column(String)
    due_date = Column(Date)
    priority = Column(String)
    status = Column(String, default="未完了")