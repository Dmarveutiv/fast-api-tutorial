from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange



app = FastAPI()

my_posts = [{"title" : "My first post", "content" : "This is my first post", "id" : 1, "date":"april 2026"}, 
            {"title": "My 2nd post", "content": "This is my 2nd post", "id": 2, "date":"june 2026"},
            {"title": "My 3rd post", "content": "This is my third post", "id": 3, "date":"may 2026"}]


class Post(BaseModel):
    title : str
    content : str
    date : str
    published : bool = True
    rating : Optional[int] = None
    
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
@app.get("/")  # home route
def root():
    return {"message" : "Hello World"}

@app.get("/posts")  # route
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")                       #path with path parameter
def get_post(id: int, response : Response ):  #path operation function
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id '{id}' was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"msg": f"Post with the id '{id}' was not found"}
    return {"post detail": post}


@app.post("/posts")
def create_post(post: Post):  #path operation function
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": my_posts}
    

