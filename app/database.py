from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_pass=os.getenv('DB_pass')
db_host=os.getenv('DB_host')
db_user=os.getenv('DB_user')
db=os.getenv('DB')
url = os.getenv('DATABASE_URL')

# SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_pass}@{db_host}/{db}'
DATABASE_URL = url
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")


engine = create_engine(DATABASE_URL)  #connect orm to db

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #connect orm to py app

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()