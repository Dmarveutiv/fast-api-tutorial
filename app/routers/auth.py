from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserLogin
from app.models import User
from app.utilis import verify


router = APIRouter(
    tags=['Authentication']
)


@router.post("/login")
def login(user_credientials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credientials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')
        
    if not verify(user_credientials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')
        
        
    return {"token" : "This is your token"}
        
        