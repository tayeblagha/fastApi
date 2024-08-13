from typing import Optional, List
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import logging
from . import models ,utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schema import Post, PostCreate, PostResponse, UserCreate, UserOut
from .utils import hash_password
from .routers import user,post
app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

# Automatic creation of tables 
models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

app.include_router(post.router)
app.include_router(user.router)