from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange



app = FastAPI()

my_posts = [{"title" : "My first post", "content" : "This is my first post", "id" : 1, "date":"april 2026"}, 
            {"title": "My 2nd post", "content": "This is my 2nd post", "id": 2, "date":"june 2026"}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    

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

@app.get("/posts/{id}")
def get_post(id):
    post = find_post(int(id))
    return {"post detail": post}

    

@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": my_posts}
    

