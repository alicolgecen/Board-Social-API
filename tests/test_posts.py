from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    post_maplist = list(map(validate, response.json()))

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client):
    response = authorized_client.get(f"/posts/115511141144")
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("Awesome new title", "Awesome content under the awesome title", True),
    ("Favorite day", "Is the one that I get 15 hours of sleep", False)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json = {
        "title": title,
        "content": content,
        "published": published
    })
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]