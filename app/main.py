from fastapi import FastAPI
from app.api.endpoints import router
from app.config import settings
from app.utils.logging.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Tron Wallet Info Service",
    description="Microservice for retrieving Tron wallet information",
    version="1.0.0",
    docs_url="/api/docs",  
    redoc_url="/api/redoc",  
    openapi_url="/api/openapi.json",
)

app.include_router(router, prefix="/api")

@app.get("/", include_in_schema=False) 
async def health_check():
    return {"status": "ok"}