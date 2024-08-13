# Data model for posts
from datetime import datetime
from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 

class PostResponse(PostBase):
    created_at: datetime
    # class Config:
    #     orm_mode=True]

class UserCreate(BaseModel):
    email:EmailStr
    password:str
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    class Config:
        from_attributes=True
    

 