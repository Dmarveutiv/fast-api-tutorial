from app import schemas
import pytest
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('key')
algo = os.getenv('algo')

if not key:
    raise ValueError("SECRET_KEY environment variable is not set!")

SECRET_KEY = key
ALGORITHM= algo



@pytest.fixture
def login_user(client):
    user_data = {"email": "kdee@gmail.com", "password": "200"}
    res = client.post('/users/', json=user_data)
      
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    new_user['email'] = user_data['email']
    return new_user

# def test_root(client, session):s
#     res = client.get('/')
#     print(res.json().get('message'))
    
def test_user(client, session):
    res = client.post('/users',
                      json={"email": "kdee@gmail.com", "password": "2005"})
    
    new_user = schemas.User(**res.json())
    assert new_user.email == 'kdee@gmail.com'
    assert res.status_code == 201
    
def test_login(client, login_user):
    res = client.post('/login',
                      data={"username": login_user['email'], "password": login_user['password']})
    login_res = schemas.Token(**res.json())
    
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id : int | None = payload.get("user_id")
    
    assert id == login_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200