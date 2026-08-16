from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.database import get_db, Base
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

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

Base.metadata.create_all(bind=engine)


def over_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        

app.dependency_overrides[get_db] = over_get_db


client = TestClient(app)

def test_root():
    res = client.get('/')
    print(res.json().get('message'))
    
def test_user():
    res = client.post('/users',
                      json={"email": "kdee@gmail.com", "password": "2005"})
    
    new_user = schemas.User(**res.json())
    assert new_user.email == 'kdee@gmail.com'
    assert res.status_code == 201