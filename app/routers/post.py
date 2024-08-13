from typing import  List
from fastapi import Body, Depends,  Response, status, HTTPException,APIRouter
from .. import models 
from ..database import  get_db
from sqlalchemy.orm import Session
from ..schema import  PostCreate, PostResponse

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )
# Get all Posts
@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.id).all()
    return posts

# Create a Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single Post
@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# Update a Post
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Update the existing post with the new values
    for key, value in post.dict().items():
        setattr(existing_post, key, value)
    
    db.commit()
    db.refresh(existing_post)  # Ensure the updated instance is returned
    return existing_post

# Delete a single Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    db.delete(existing_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


