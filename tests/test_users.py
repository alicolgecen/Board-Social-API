from jose import jwt
from app import schemas
from app.config import settings
import pytest 

def test_create_user(client):
    response = client.post("/users/", json = {
        "email" : "test@test.co",
        "password" : "testing123" 
    })
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test@test.co"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/login", data= {
        "username" : test_user["email"],
        "password" : test_user["password"]
        })
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms= [settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@aa.dd", "testing123", 403),
    ("test@test.co", "wahoo", 403),
    ("wrongemail@aa.dd", "wahoo", 403),
    (None, "testing123", 422),
    ("test@test.co", None, 422)
    ])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/login", data = {
        "username": email,
        "password": password
    })
    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid credentials!"