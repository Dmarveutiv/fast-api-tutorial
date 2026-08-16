from app import schemas
from .database import client, session
    
def test_root(client, session):
    res = client.get('/')
    print(res.json().get('message'))
    
def test_user(client, session):
    res = client.post('/users',
                      json={"email": "kdee@gmail.com", "password": "2005"})
    
    new_user = schemas.User(**res.json())
    assert new_user.email == 'kdee@gmail.com'
    assert res.status_code == 201