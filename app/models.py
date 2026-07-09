from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primarykey=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published =  Column(Boolean, default=True)