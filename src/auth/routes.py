from fastapi import APIRouter ,Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserCreateModel, UserLoginModel, ForgotPasswordModel, ResetPasswordModel
from src.auth.service import AuthService
from src.db.database import get_db
from src.auth.dependencies import get_current_user


router = APIRouter()
service = AuthService()


@router.get("/profile")
async def profile(current_user = Depends(get_current_user)):
    return current_user


@router.post("/signup")
async def signup(data:UserCreateModel, db: AsyncSession = Depends(get_db)):
    return await service.signup(data, db)


@router.post("/login")
async def login(data: UserLoginModel, db: AsyncSession = Depends(get_db)):
    user = await service.login(data, db)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user


#---------Forget Password---------------#
@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordModel, db:AsyncSession = Depends(get_db)):
    return await service.forgot_password(data.email, db)


#----------Reset Password------------#
@router.post("/reset-password")
async def reset_password(data: ResetPasswordModel, db:AsyncSession = Depends(get_db)):
    return await service.reset_password(
        data.token,
        data.new_password,
        db
    )
    
    

 
