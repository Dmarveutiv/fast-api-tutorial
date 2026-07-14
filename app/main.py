from app import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time
from app.database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from pwdlib import PasswordHash


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# load_dotenv()

# db_pass=os.getenv('DB_pass')
# db_host=os.getenv('DB_host')
# db_user=os.getenv('DB_user')
# db=os.getenv('DB')

# while True:
#     try:
#         conn = psycopg2.connect(host=db_host,
#                             database=db,
#                             user=db_user,
#                             password=db_pass, 
#                             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()   #allows us to run sql queries
#         print("Succesfully conected to database")
#         break
#     except Exception as error:
#          print("failed to connect to database")
#          print("Error:", error)
#          time.sleep(3)

        
@app.get("/")  # home route
def root():
    return {"message" : "Hello World"}

@app.get("/posts", response_model=List[schemas.Post])  # route
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.Post)                       #path with path parameter
def get_post(id: int, db : Session = Depends(get_db)):  #path operation function
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id '{id}' was not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):  #path operation function
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id =%s RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with the id of '{id}' does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s
    #                 WHERE id = %s RETURNING * """, 
    #                 (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    up_post = post_query.first()
    if up_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with the id of '{id}' does not exist")
        
    post_query.update(post.dict(), synchronize_session=False)
    
    db.commit()
        
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)  
def create_user( user: schemas.UserCreate,     db: Session = Depends(get_db)):
    
    # hashed_password =  pwd_context.hash(user.password[:72])
    # user.password = hashed_password
    password_hash = PasswordHash.recommended()
    user.password = password_hash.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
