from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data model for posts
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Connect to the database and apply a script
def apply_script(script: str, args: Optional[tuple] = None):
    try:
        with psycopg.connect("dbname=fastapi user=postgres password=root") as conn:
            with conn.cursor() as cur:
                cur.execute(script, args)
                print(args)
                result = cur.fetchall() if args is None   else None
                conn.commit()
                return result
    except psycopg.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
def apply_script_id(script: str, args: Optional[tuple] = None):
    try:
        with psycopg.connect("dbname=fastapi user=postgres password=root") as conn:
            with conn.cursor() as cur:
                cur.execute(script, args)
                print(args)
                result = cur.fetchall() 
                conn.commit()
                return result
    except psycopg.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
def get_posts():
    result = apply_script("SELECT * FROM posts order by id")
    
    return result

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    values = post.dict()
    try:
        apply_script('INSERT INTO posts (title, content) VALUES (%s, %s)', (values["title"], values["content"]))
        return get_posts()
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating post")

@app.get("/posts/{id}")
def get_post(id: int):
    result = apply_script_id("SELECT * FROM posts WHERE id = %s", (id,))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return result[0]

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    existing_post = apply_script_id("SELECT * FROM posts WHERE id = %s", (id,))
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    updated_values = post.dict()
    try:
        apply_script(
            "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
            (updated_values["title"], updated_values["content"], updated_values["published"], id)
        )
        return {"message": "Post updated successfully"}
    except Exception as e:
        logger.error(f"Error updating post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating post")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    existing_post = apply_script_id("SELECT * FROM posts WHERE id = %s", (id,))
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    try:
        apply_script("DELETE FROM posts WHERE id = %s", (id,))
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error deleting post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting post")
