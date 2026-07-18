import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from app.schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


load_dotenv()
secret_key = os.environ.get('key')
algorithm = os.getenv('algo')

if not secret_key:
    raise ValueError("SECRET_KEY environment variable is not set!")

SECRET_KEY = secret_key
ALGORITHM = algorithm
ACCESS_TOKEN_EXPIRES_MINUTES = 30

def create_access_token(data : dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token : str, credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : int | None = payload.get("user_id")
    
        if id is None:
            raise credentials_exception
    
        token_data = TokenData(id= id)
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="Could not validate credentials",
                                            headers={"WWW-Authenticate": "Bearer"},
    )
    
    return verify_access_token(token, credentials_exception)
        
        
    
