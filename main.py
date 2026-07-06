from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional



app = FastAPI()

my_posts = [{"title" : "My first post", "content" : "This is my first post", "id" : 1}, 
            {"title": "My 2nd post", "content": "This is my 2nd post", "id": 2}]

class Post(BaseModel):
    title : str
    content : str
    date : str
    published : bool = True
    rating : Optional[int] = None
    

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_post(post: Post):
    return {"data": post}
    

