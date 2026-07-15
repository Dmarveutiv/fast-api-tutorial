from .. import models, schemas, utilis
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)  
def create_user( user: schemas.UserCreate,     db: Session = Depends(get_db)):
    
    password_hash = utilis.hash(user.password)
    user.password = password_hash
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/users/{id}", response_model=schemas.User)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with the id of {id}, does not exist')
    
    return user