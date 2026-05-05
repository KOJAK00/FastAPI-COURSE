from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException,Request,Depends
from src.user.dtos import UserSchema,loginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.utils.settings import settings
from pwdlib import PasswordHash
from datetime import datetime,timedelta
import jwt
from jwt.exceptions import InvalidTokenError
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
EXP_TIME = 30

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(body : UserSchema , db : Session):
    data=body.model_dump()
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400,"A user with this username or email already exists.")
    
    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(400,"A user with this username or email already exists.")
    
    hash_password = get_password_hash(body.password)
    
    new_uesr = UserModel(
        name = data["name"],
        username = data["username"],
        hash_password = hash_password,
        email = data["email"]
    )
    db.add(new_uesr)
    db.commit()
    db.refresh(new_uesr)
    return new_uesr

def login_user(db: Session, body: OAuth2PasswordRequestForm = Depends()):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(status_code=401, detail="invalid credentials")

    exp_time = datetime.utcnow() + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode(
        {"__id": user.id, "exp": exp_time},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHIM
    )

    return {"access_token": token, "token_type": "bearer"}

