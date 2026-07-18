from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserLogin, Token
from app.models import User
from app.utilis import verify
from app.oauth2 import create_access_token


router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=Token)
def login(user_credientials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credientials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
        
    if not verify(user_credientials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
        
    
    
    access_token = create_access_token({"user_id" : user.id})   
    return {"access_token": access_token, "token_type": "bearer"}
        
        