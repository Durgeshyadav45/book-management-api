from pydantic import BaseModel, EmailStr


class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    
class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
    
    
class ForgotPasswordModel(BaseModel):
    email: EmailStr
    
    
class ResetPasswordModel(BaseModel):
    token: str
    new_password: str





    