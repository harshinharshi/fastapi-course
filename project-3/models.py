from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__: str = 'todos'
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    title: Column[str] = Column(String)
    description: Column[str] = Column(String)
    priority: Column[int] = Column(Integer)
    complete: Column[bool] = Column(Boolean, default=False)