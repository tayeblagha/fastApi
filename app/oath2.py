from datetime import datetime, timedelta
from msilib import schema
from fastapi import Depends, HTTPException
from  jose import jwt,JWTError

from .database import get_db
from . import schema,models
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import logging
from .schema import TokenData
from .config import settings
from fastapi.security import OAuth2PasswordBearer
oath2_scheme= OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data:dict):
    to_encode= data.copy()
    expire=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode,settings.SECRET_KEY,settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload= jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)
        id:str=payload.get("user_id")
        if id==None :
            print("null ID")
            raise credentials_exception
        token_data=TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data
def get_current_user(token:str=Depends(oath2_scheme),db: Session = Depends(get_db)):
    credentials_exception =HTTPException (
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"not validated credentials",
        headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user
    
    
    