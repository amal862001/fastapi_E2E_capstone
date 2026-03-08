from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from config import settings
from routers.auth import router as auth_router
from routers.complaints import router as complaints_router



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

# register routers
app.include_router(auth_router)
app.include_router(complaints_router)

@app.get("/")
def root():
    return {"message": "NYC 311 API is running"}


