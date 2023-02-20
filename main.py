from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

class UpdatePost(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


posts = [
    {"id": 1, "title": "title of post 1", "content": "content of post 1"},
    {"id": 2, "title": "favorite foods", "content": "pizza for example"}
    ]

def find_post (id):
    for p in posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to my API."}

@app.get("/posts")
def get_posts():
    return {"data": posts}

@app.post("/posts")
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,100000000)
    posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id:int, response:Response):
    post = find_post(int(id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} was not found!")
    return {
        "post_detail": post
        }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist!")
    posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:UpdatePost):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist!")
    post_dict = post.dict()
    post_dict["id"] = id
    posts[index] = post_dict
    return {
        "data": post_dict
    }

# 02:18:00'da kaldım