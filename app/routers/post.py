from typing import  List, Optional
from fastapi import Body, Depends,  Response, status, HTTPException,APIRouter
from sqlalchemy import func
from .. import models , oath2
from ..database import  get_db
from sqlalchemy.orm import Session
from ..schema import  PostCreate, PostResponse, PostVotes

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )
# Get all Posts
@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):
    posts = (
    db.query(models.Post)
    .filter(models.Post.title.like(f"%{search}%"))
    .order_by(models.Post.id)
    .offset(skip)
    .limit(limit)
)
    return posts

# Create a Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db),current_user:int=Depends(oath2.get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.user_id=current_user.id
    db.add(new_post)
    db.commit()
    print(current_user.email)
    db.refresh(new_post)
    return new_post

# Get a single Post
# Get a single Post
@router.get("/{id}", response_model=PostVotes)
def get_post(id: int, db: Session = Depends(get_db)):
    # Fetch the post
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Fetch the number of likes for the post
    vote_count = db.query(func.count(models.Vote.user_id)).filter(models.Vote.post_id == id).scalar()
    
    # Construct the response model with the post data and vote count
    response_post = PostVotes(
        id=post.id,
        title=post.title,
        content=post.content,  # Include other fields as needed
        vote_count=vote_count
    )
    
    return response_post

# Update a Post
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db),current_user:int=Depends(oath2.get_current_user)):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Update the existing post with the new values
    
    if existing_post.user_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are unable to update others post")

        
    for key, value in post.dict().items():
        setattr(existing_post, key, value)
    
    db.commit()
    db.refresh(existing_post)  # Ensure the updated instance is returned
    return existing_post

# Delete a single Post
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db),current_user:int=Depends(oath2.get_current_user)):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    print(existing_post.user_id,current_user.id)
    if existing_post.user_id==current_user.id:
        db.delete(existing_post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are unable to delete others post")


