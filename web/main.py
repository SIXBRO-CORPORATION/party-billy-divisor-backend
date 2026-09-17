import logging
from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from persistence.database import close_db
from security.config import settings
from web.commons.exception_handler import register_exception_handler
from web.controllers.auth_controller import router as auth_router


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting API")

    yield

    logger.info("Shutting down API")
    await close_db()


app = FastAPI(
    title="Billy API",
    description="Bill Divisor",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        settings.frontend_url
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handler(app)

app.include_router(auth_router)


async def root():
    return {"status": "ok", "message": "API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected", "pool": "active"}


if __name__ == "__main__":
    uvicorn.run(
        "web.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
