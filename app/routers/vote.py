from typing import  List, Optional
from fastapi import Body, Depends,  Response, status, HTTPException,APIRouter

from .. import oath2
from .. import models 
from ..database import  get_db
from sqlalchemy.orm import Session
from ..schema import  VoteCreate,VoteResponse

router = APIRouter(
    prefix="/vote",
    tags=["Vote System"]
    )


# Create or update a vote
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_or_update_vote(
    vote_create: VoteCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oath2.get_current_user)
):
    existing_post = db.query(models.Post).filter(models.Post.id == vote_create.post_id).first()
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")

    # Check if a vote already exists for the given post and user
    existing_vote = db.query(models.Vote).filter(
        models.Vote.post_id == vote_create.post_id,
        models.Vote.user_id == current_user.id
    ).first()
    
    if vote_create.state == 1:
        if existing_vote is None:
            # Create a new vote
            new_vote = models.Vote(
                post_id=vote_create.post_id,
                user_id=current_user.id
            )
            db.add(new_vote)
            db.commit()
            return {"message": "Vote successfully added"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Post already voted")
    elif vote_create.state == 0:
        if existing_vote is not None:
            # Delete existing vote if state is 0
            db.delete(existing_vote)
            db.commit()
            return {"message": "You have successfully unvoted for the post"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Post not voted yet")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote state")

