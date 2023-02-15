from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

#Path operation
@app.get("/") #Decorator
def root(): #Function
    return {"message": "Welcome to my API."}

@app.get("/posts")
def get_posts():
    return {"data": "Here are your posts."}

@app.post("/createpost")
def create_post(post:Post):
    print(post)
    print(post.dict())
    return {"data": post}

# 1:22:48'de kaldım.