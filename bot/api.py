import logging
from contextlib import asynccontextmanager

from aiogram import Bot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from bot.config import ADMIN_CHAT_ID, BOT_TOKEN, DATABASE_URL
from bot.db.leads import init_db, save_lead

logger = logging.getLogger(__name__)

SUMMARY = (
    "🌐 Заявка с сайта\n\n"
    "👤 Имя: {name}\n"
    "📞 Телефон: {phone}\n"
    "💬 Сообщение: {message}"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if DATABASE_URL:
        await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://alga.world", "https://www.alga.world"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class LeadIn(BaseModel):
    name: str
    phone: str
    message: str


@app.post("/lead")
async def create_lead(data: LeadIn):
    await save_lead(
        name=data.name,
        phone=data.phone,
        service="Сайт",
        message=data.message,
        lang="ru",
    )
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(
            ADMIN_CHAT_ID,
            SUMMARY.format(name=data.name, phone=data.phone, message=data.message),
        )
    except Exception:
        logger.exception("Failed to notify admin")
    finally:
        await bot.session.close()
    return {"ok": True}
