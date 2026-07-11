from app import models
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time
from app.database import engine, get_db
from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


load_dotenv()

db_pass=os.getenv('DB_pass')
db_host=os.getenv('DB_host')
db_user=os.getenv('DB_user')
db=os.getenv('DB')

while True:
    try:
        conn = psycopg2.connect(host=db_host,
                            database=db,
                            user=db_user,
                            password=db_pass, 
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()   #allows us to run sql queries
        print("Succesfully conected to database")
        break
    except Exception as error:
         print("failed to connect to database")
         print("Error:", error)
         time.sleep(3)
    


class Post(BaseModel):
    title : str
    content : str
    published : bool = True

        
@app.get("/")  # home route
def root():
    return {"message" : "Hello World"}

@app.get("/sql")
def test_post(db: Session = Depends(get_db)):
    pass

@app.get("/posts", )  # route
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts/{id}")                       #path with path parameter
def get_post(id: int):  #path operation function
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id '{id}' was not found")
    return {"post detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):  #path operation function
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    
    conn.commit()
    
    return {"data": new_post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id =%s RETURNING * """, (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s
                    WHERE id = %s RETURNING * """, 
                    (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post does not exist")
        
    return {"data": updated_post}
    
    
    
