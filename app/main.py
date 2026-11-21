from app.products import router as products_router
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.analytics import router as analytics_router

from app.database import engine

app = FastAPI(
    title="Smart Retail Sales Intelligence API",
    description="API for retail sales analytics",
    version="1.0.0"
)

app.include_router(products_router)
app.include_router(analytics_router)
@app.get("/")
def home():
    return {
        "message": "Welcome to Smart Retail Sales Intelligence API"
    }


@app.get("/health")
def health():
    return {
        "status": "API is running successfully"
    }


@app.get("/health/db")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "Connected",
            "database": "PostgreSQL"
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )

