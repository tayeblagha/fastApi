from .. import schema
from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, Response, status,APIRouter
import logging

from fastapi.security import OAuth2PasswordRequestForm

from .. import oath2
from .. import models ,utils
from ..database import  get_db
from sqlalchemy.orm import Session
from ..schema import  UserLogin
from ..utils import hash_password
router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
    )

@router.post("/",response_model=schema.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    new_user = user_credentials
    user = db.query(models.User).filter(models.User.email == new_user.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not  utils.verify_password(new_user.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials") 
    # create a token 
    access_token=oath2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token, "token_type": "bearer"}