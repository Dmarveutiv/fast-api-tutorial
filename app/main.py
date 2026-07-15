from app import models
from fastapi import FastAPI
from app.database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# load_dotenv()

# db_pass=os.getenv('DB_pass')
# db_host=os.getenv('DB_host')
# db_user=os.getenv('DB_user')
# db=os.getenv('DB')

# while True:
#     try:
#         conn = psycopg2.connect(host=db_host,
#                             database=db,
#                             user=db_user,
#                             password=db_pass, 
#                             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()   #allows us to run sql queries
#         print("Succesfully conected to database")
#         break
#     except Exception as error:
#          print("failed to connect to database")
#          print("Error:", error)
#          time.sleep(3)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
        
@app.get("/")  # home route
def root():
    return {"message" : "Hello World"}


