# Data model for posts
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, conint

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True

class UserInfo(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class PostResponse(PostBase):
    created_at: datetime
    user_id: int
    user: UserInfo
class PostVotes(PostBase):
    vote_count:int=0

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    #posts: List[PostBase]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True

class VoteCreate(BaseModel):
    post_id:int
    state: conint(ge=0, le=1)  # ge=0 (greater than or equal to 0) and le=1 (less than or equal to 1)
class VoteResponse(BaseModel):
    user_id:int
    post_id:int
    
    
    