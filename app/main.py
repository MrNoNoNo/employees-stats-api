from fastapi import FastAPI

from app.api import endpoints

app = FastAPI(
    title="Employee Statistics API",
    description="API for querying statistical summaries and distributions from an employee dataset.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(endpoints.router)
