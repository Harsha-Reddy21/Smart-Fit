import uvicorn
from fastapi import FastAPI


app = FastAPI()

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
