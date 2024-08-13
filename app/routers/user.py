from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, Response, status,APIRouter
import logging
from .. import models ,utils
from ..database import  get_db
from sqlalchemy.orm import Session
from ..schema import  UserCreate, UserOut
from ..utils import hash_password
router = APIRouter(
    prefix="/users",
    tags=["Users"]
    )

# Get all Users
@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id).all()
    return users

# Get a single User by ID
@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
# Create a User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        # Return an HTTP 400 Bad Request with a specific error detail
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user.password=hash_password(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# Update a User
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_user(id: int, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.id == id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Update the existing user with the new values
    for key, value in user.dict().items():
        setattr(existing_user, key, value)
    
    db.commit()
    db.refresh(existing_user)  # Ensure the updated instance is returned
    return existing_user

# Delete a User
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.id == id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(existing_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
