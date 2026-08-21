from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from app.oauth2 import create_access_token
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app import models

load_dotenv()

db_pass=os.getenv('DB_pass')
db_host=os.getenv('DB_host')
db_user=os.getenv('DB_user')
db=os.getenv('DB')
url = os.getenv('DATABASE_URL')

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_pass}@{db_host}/{db}'
# DATABASE_URL = url
# if DATABASE_URL:
#     DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

engine = create_engine(SQLALCHEMY_DATABASE_URL) #connect orm to db
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #connect orm to py app


@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
            yield db
    finally:
            db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(session):
    def over_get_db():
    
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = over_get_db
    yield TestClient(app)
    
@pytest.fixture
def login_user(client):
    user_data = {"email": "kdee@gmail.com", "password": "200"}
    res = client.post('/users/', json=user_data)
      
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    new_user['email'] = user_data['email']
    return new_user

@pytest.fixture
def token(login_user):
    return create_access_token({"user_id": login_user['id']})

@pytest.fixture
def authorized_client(token, client):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token} '
    }
    
    return client

@pytest.fixture
def put_posts(login_user, session):
    posts_data = [
        {
            "title": "title 1",
            "content": "content 1",
            "owner_id": login_user['id']
        },
        {
            "title": "title 2",
            "content": "content 2",
            "owner_id": login_user['id']
        },
                {
            "title": "title 3",
            "content": "content 3",
            "owner_id": login_user['id']
        }
        
    ]
    
    def create_post_model(post):
       x =  models.Post(**post)
       
       return x
        
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()
    
    posts = session.query(models.Post).all()
    
    return posts