from app import schemas
from .database import client, session
import pytest


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
    
    assert res.status_code == 200