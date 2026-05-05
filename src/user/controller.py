from fastapi import HTTPException,Request
from src.user.dtos import UserSchema,loginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.utils.settings import settings
from pwdlib import PasswordHash
from datetime import datetime,timedelta
import jwt
from jwt.exceptions import InvalidTokenError
password_hash = PasswordHash.recommended()
EXP_TIME = 30

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(body : UserSchema , db : Session):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400,"Username already exist")
    
    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(400,"Email already exist")
    
    hash_password = get_password_hash(body.password)

    new_uesr = UserModel(
    name = body.name,
    username = body.username,
    hash_password = hash_password,
    email = body.email
    )
    db.add(new_uesr)
    db.commit()
    db.refresh(new_uesr)
    return new_uesr

def login_user(body: loginSchema,db:Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(404,"invalid credentials")
    
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(404,"invalid credentials")
    
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"__id":user.id,"exp":exp_time.timestamp()},settings.SECRET_KEY,settings.ALGORITHIM)
    return {"token":token}

