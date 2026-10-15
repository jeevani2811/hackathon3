import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.session import init_db, AsyncSessionLocal
from backend.app.models import User
from backend.app.security.auth import hash_password
from backend.app.api.v1 import api_router
from sqlalchemy import select

# Pre-seed default demo analyst user if database is empty
async def seed_initial_data():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).where(User.email == "analyst@enterprise.ai"))
        if not res.scalars().first():
            demo_user = User(
                id="usr-demo-001",
                email="analyst@enterprise.ai",
                hashed_password=hash_password("demo1234"),
                full_name="Lead Strategy Analyst",
                role="lead_analyst"
            )
            db.add(demo_user)
            await db.commit()
            logger.info("Seeded default demo analyst credentials into database.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting OmniAgent Intelligent Systems Backend...")
    await init_db()
    await seed_initial_data()
    yield
    logger.info("Shutting down OmniAgent Backend...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Autonomous multi-agent system for enterprise market intelligence, strategic decision-making, and financial TCO analysis.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=r"^https:\/\/.*\.vercel\.app$|^http:\/\/localhost(:\d+)?$|^http:\/\/127\.0\.0\.1(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OPERATIONAL",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR,
        "documentation": "Visit /docs for OpenAPI interactive specification."
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception intercepted at {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal system error occurred. Please refer to operational logs."}
    )
