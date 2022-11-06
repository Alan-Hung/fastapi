from fastapi import FastAPI
from app import models, database
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# Create all models (i.e. tables)
# Replace by alembic
# models.database.Base.metadata.create_all(bind=database.Engine)

app = FastAPI()

origins = ["https://www.google.com.tw",
           "http://localhost.tiangolo.com",
           "https://localhost.tiangolo.com",
           "http://localhost",
           "http://localhost:8000",
           ]

# CROC rule (allow access from different domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "hello world"}

app.include_router(post.Router)
app.include_router(user.Router)
app.include_router(auth.Router)
app.include_router(vote.Router)




