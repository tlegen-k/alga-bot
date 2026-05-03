import logging
from bot.db.connection import get_pool

logger = logging.getLogger(__name__)

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS leads (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    phone       TEXT NOT NULL,
    service     TEXT NOT NULL,
    message     TEXT NOT NULL,
    lang        TEXT NOT NULL DEFAULT 'kk',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


async def init_db() -> None:
    pool = await get_pool()
    await pool.execute(CREATE_TABLE)


async def save_lead(name: str, phone: str, service: str, message: str, lang: str) -> None:
    try:
        pool = await get_pool()
        await pool.execute(
            "INSERT INTO leads (name, phone, service, message, lang) VALUES ($1,$2,$3,$4,$5)",
            name, phone, service, message, lang,
        )
    except Exception:
        logger.exception("Failed to save lead to DB")
