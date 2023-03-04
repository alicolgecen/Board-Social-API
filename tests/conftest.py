from fastapi.testclient import TestClient
import pytest 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app.main import app
from app import models


# New database for testing
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# Testing part
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {
        "email" : "test@test.co",
        "password" : "testing123" 
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture()
def test_posts(test_user, session):
    posts_data = [{
        "title": "1st title",
        "content": "1st content",
        "owner_id": test_user['id']
        },
        {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
        },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user["id"]
        }]
    def create_post_model(postStructure):
        return models.Post(**postStructure)
    
    post_maplist = list(map(create_post_model, posts_data))

    session.add_all(post_maplist)
    session.commit()

    posts = session.query(models.Post).all()
    return posts

