from fastapi import APIRouter,Depends,status,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema,UserResponseSchema,loginSchema
from src.user.models import UserModel
from src.user import controller

user_routes = APIRouter(prefix="/user",tags=["user"])

@user_routes.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema,db=Depends(get_db)):
    return controller.register(body,db)

@user_routes.post("/login",status_code=status.HTTP_200_OK)
def login(body:OAuth2PasswordRequestForm=Depends(),db=Depends(get_db)):
    return controller.login_user(db,body)

@user_routes.get("/is_auth",response_model=UserResponseSchema,status_code=status.HTTP_200_OK)
def is_authenticated(request:Request,db=Depends(get_db)):
    return controller.is_authenticated(request,db)