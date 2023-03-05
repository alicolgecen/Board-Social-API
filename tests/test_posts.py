from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    post_maplist = list(map(validate, response.json()))

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client):
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
def test_create_post(authorized_client, test_user, title, content, published):
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

def test_create_post_default_published_true(authorized_client, test_user):
    response = authorized_client.post("/posts/", json = {
        "title": "blabla",
        "content": "blabla"
    })
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == "blabla"
    assert created_post.content == "blabla"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]

def test_unauthorized_user_create_post(client):
    response = client.post("/posts/", json = {
        "title": "blabla",
        "content": "blabla"
    })
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_non_exist(authorized_client):
    response = authorized_client.delete("/posts/84848948949848949848989498489489498489498498")
    assert response.status_code == 404

def test_delete_other_users_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[2].id}")

    assert response.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = schemas.PostResponse(**response.json())

    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_users_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id
    }
    response = authorized_client.put(f"/posts/{test_posts[2].id}", json = data)

    assert response.status_code == 403

def test_unauthroized_user_update_post(client, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_update_post_non_exist(authorized_client):
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    response = authorized_client.put("/posts/84848948949848949848989498489489498489498498", json=data)
    assert response.status_code == 404