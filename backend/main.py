from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.db.session import create_db_and_tables
from app.routers.auth import router as auth_router
from app.routers.exercises import router as exercises_router
from app.routers.workouts import router as workouts_router
from app.routers.nutrition import router as nutrition_router
from app.routers.progress import router as progress_router
from app.routers.chat import router as chat_router


app = FastAPI(title="SmartFit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def health_status():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(exercises_router)
app.include_router(workouts_router)
app.include_router(nutrition_router)
app.include_router(progress_router)
app.include_router(chat_router)
