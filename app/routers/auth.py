from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserLogin
from app.models import User


router = APIRouter(
    tags=['Authentication']
)


@router.post("/login")
def login(user_credientials: UserLogin, db: Session = Depends(get_db)):
    db.query(User).filter(User.email == user_credientials.email).first()