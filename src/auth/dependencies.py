from fastapi import Depends, HTTPException
from src.config import settings
from src.auth.utils import oauth2_scheme
from jose import jwt, JWTError


async def get_current_user(token:str = Depends(oauth2_scheme)):
    try: 
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



def admin_only(current_user = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user