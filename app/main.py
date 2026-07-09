from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time


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
    
    
    
my_posts = [{"title" : "My first post", "content" : "This is my first post", "id" : 1,}, 
            {"title": "My 2nd post", "content": "This is my 2nd post", "id": 2,},
            {"title": "My 3rd post", "content": "This is my third post", "id": 3,}]


class Post(BaseModel):
    title : str
    content : str
    published : bool = True

    
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        
@app.get("/")  # home route
def root():
    return {"message" : "Hello World"}

@app.get("/posts", )  # route
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
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
    index = find_index(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
        
    return {"data": post_dict}
    
    
    
