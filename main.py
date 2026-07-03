from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

posts : list[dict] = [
    {
       'id' : 1,
       'title' : "first post",
       'author' : "john doe",
       'content' : "this is my first pose",
    },
    
    {
        'id' : 2,
        'title' : "second post",
        'author' : "jane derrick",
        'content' : "this is my second post",
    },
]

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/posts")
def get_posts():
    return posts

@app.post("/createposts")
def create_post(payload : dict = Body(...)):
    return {"new_post" : f'title : {payload['title']} content : {payload['content']} '}

