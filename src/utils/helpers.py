from fastapi import HTTPException,Request,Depends
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.utils.settings import settings
from src.utils.db import get_db
import jwt
from jwt.exceptions import InvalidTokenError


def is_authenticated(request:Request,db:Session= Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(401,"You are unauthrized")
        token = token.split(" ")[-1]
        
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHIM)
        user_id = data.get("__id")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not user:
            raise HTTPException(401,"You are unauthrized")
        
        return user
    
    except InvalidTokenError:
        raise HTTPException(401,"You are unauthrized")