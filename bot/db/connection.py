import asyncpg
from bot.config import DATABASE_URL

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        dsn = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        _pool = await asyncpg.create_pool(dsn)
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
