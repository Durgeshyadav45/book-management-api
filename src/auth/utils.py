from src.config import settings
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer



pwd_context = CryptContext(schemes=["bcrypt"])


#--------JWT Token extractor----------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed_password ):
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_data: dict):
    expire = datetime.utcnow() + timedelta (minutes=30)
    
    payload = {
        **user_data,
        "exp": expire
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return token



def create_reset_token (email: str):
    expire = datetime.utcnow() + timedelta(minutes=15)
    
    payload = {
        "sub": email,
        "exp": expire,
        "scope": "password_reset"
    }
    
    token = jwt.encode (
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token



def verify_reset_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=settings.JWT_ALGORITHM
        )
        
        if payload.get("scope") != "password_reset":
            return None
        return payload.get("sub")
    
    except JWTError:
        return None







