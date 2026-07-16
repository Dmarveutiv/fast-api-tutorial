import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


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
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt