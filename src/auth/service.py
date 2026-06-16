from fastapi import HTTPException
from sqlalchemy import select
from src.auth.models import User
from src.auth.utils import hash_password, verify_password, create_access_token, create_reset_token,verify_reset_token

class AuthService:
    
    async def signup(self, user_data, db):
        statement = select(User).where(User.email == user_data.email)
        result = await db.execute(statement)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            return{
                "massage": "user already exists"
            }
        
        new_user = User(
            username = user_data.username,
            email = user_data.email,
            password_hash = hash_password(user_data.password)
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user
    
    
    async def login(self, user_data, db):
        statement = select(User).where(User.email == user_data.email)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()
        
        if not user:
            return {
                "message": "Invalid Email"
            }
        
        password_valid = verify_password(user_data.password, user.password_hash)
        
        if not password_valid:
            return{
                "message": "Invalid password"
            }
            
            
        assess_token = create_access_token(
            user_data={
                "user_id": user.id,
                "email": user.email,
                "role": user.role
            }
        )
        return{
            "access_token": assess_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role" : user.role
            }
        }
        
async def forgot_password(self , email: str, db):
    user = await self.user_exists(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    token = create_access_token(user.email)
    return{
        "reset_token": token
    }
        
        
async def reset_passord(self, token:str, new_password:str, db):
    email = verify_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
        
    user = await self.user_exists(email,db)
    user.password = hash_password(new_password)
    
    await db.commit()
    return{
        "message": "password reset successful"
    }
        

















# from .models import User
# from .schemas import UserCreateModel
# from .utils import generate_passwd_hash
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlmodel import select


# class UserService:
#     @staticmethod
#     async def get_user_by_email( email:str, session: AsyncSession):
#         statement = select(User).where(User.email == email)
        
#         result = await session.execute(statement)
#         user = result.scalar_one_or_none()
#         return user
    
    
#     @staticmethod
#     async def user_exists(email:str, session: AsyncSession):
#         user = await UserService.get_user_by_email(email,session)
#         return user is not None
        
       
#     @staticmethod
#     async def create_user( user_data: UserCreateModel, session:AsyncSession):
#         user_data_dict = user_data.model_dump()
        
#         new_user = User(
#             username=user_data_dict['username'],
#             email=user_data_dict['email']
#         )
        
#         new_user.password_hash = generate_passwd_hash(user_data_dict['password'])
#         session.add(new_user)
#         await session.commit()
#         await session.refresh(new_user)
        
#         return new_user