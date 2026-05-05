from pydantic import BaseModel,EmailStr

class UserSchema(BaseModel):
    name : str
    username : str
    password : str
    email : EmailStr

class UserResponseSchema(BaseModel):
    name : str
    username : str
    email : EmailStr    
    id : int

class loginSchema(BaseModel):
    username : str
    password : str