from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from config import settings

# create database engine
engine = create_engine(settings.DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup - test database connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Database connected")
    yield
    # shutdown
    engine.dispose()
    print("Database disconnected")

app = FastAPI(
    title="NYC 311 API",
    description="Internal API for NYC agency staff to manage 311 complaints",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "NYC 311 API is running"}
