import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.base import Base

# Ensure data directories exist
os.makedirs("backend/data", exist_ok=True)
os.makedirs("backend/data/artifacts", exist_ok=True)

def resolve_database_url() -> str:
    raw_url = settings.DATABASE_URL.strip()
    
    # Check if placeholder is present (e.g. user hasn't replaced password/ref yet)
    is_placeholder = any(
        ph in raw_url for ph in [
            "<your-password>", 
            "[YOUR-PASSWORD]", 
            "<your-supabase-password>", 
            "[YOUR-PROJECT-REF]", 
            "<project-ref>"
        ]
    )
    if is_placeholder:
        logger.warning(
            "Detected placeholder in Supabase DATABASE_URL. "
            "Falling back to local SQLite database until real credentials are provided in .env."
        )
        return "sqlite+aiosqlite:///backend/data/omniagent.db"

    # Normalize standard postgresql:// or postgres:// to postgresql+asyncpg://
    if raw_url.startswith("postgresql://"):
        raw_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+asyncpg://", 1)

    return raw_url

db_url = resolve_database_url()

# Configure engine connection parameters
connect_args = {}
engine_kwargs = {"echo": False, "future": True}

if "sqlite" in db_url:
    connect_args["check_same_thread"] = False
elif "postgresql+asyncpg" in db_url:
    # Supabase Transaction Pooler (port 6543) requires disabling statement cache
    if ":6543" in db_url or "pooler" in db_url:
        connect_args["statement_cache_size"] = 0
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_async_engine(
    db_url,
    connect_args=connect_args,
    **engine_kwargs
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f"Database schema initialized successfully on: {db_url.split('@')[-1] if '@' in db_url else 'local SQLite'}")
    except Exception as e:
        logger.error(f"Failed initializing database tables: {str(e)}", exc_info=True)
        raise
