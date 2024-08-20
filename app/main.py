
from fastapi import  FastAPI
import logging

from . import models 
from .database import engine
from .routers import user,post,auth,vote
app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 
from .config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


# Automatic creation of tables 
models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)