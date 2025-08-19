from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.get("/health")
def health_status():
    return {"App is Working"}










@app.post('/auth/register')
def register():
    "User Registration"

@app.post('/auth/login')
def login():
    "User login"


@app.get('/auth/user{user_id}')
def get_user():
    "Get User Profile"


@app.post('/chat/ask')
def generate_answer():
    "Send question, get rag-powered response"


@app.get('/chat/history{user_id}')
def get_chat_history():
    "Get chat history of user"
