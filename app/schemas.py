from pydantic import BaseModel, EmailStr
from datetime import datetime
    
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class PostCreate(PostBase):
    pass
    
class Post(PostBase):
    created_at : datetime
    
    
class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
class User(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
class Config:
    from_attributes = True
    