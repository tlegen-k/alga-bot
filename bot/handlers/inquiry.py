import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from bot.i18n import get_text
from bot.db.leads import save_lead
from bot.config import ADMIN_CHAT_ID

router = Router()
logger = logging.getLogger(__name__)


class InquiryForm(StatesGroup):
    lang = State()
    name = State()
    phone = State()
    service = State()
    message = State()


def _lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="lang:kk"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        InlineKeyboardButton(text="🇬🇧 English",  callback_data="lang:en"),
    ]])


def _service_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("service_website", lang),    callback_data="service:website"),
            InlineKeyboardButton(text=get_text("service_bot", lang),        callback_data="service:bot"),
        ],
        [
            InlineKeyboardButton(text=get_text("service_automation", lang), callback_data="service:automation"),
            InlineKeyboardButton(text=get_text("service_other", lang),      callback_data="service:other"),
        ],
    ])


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(InquiryForm.lang)
    await message.answer(get_text("choose_lang", "kk"), reply_markup=_lang_keyboard())


@router.callback_query(InquiryForm.lang, F.data.startswith("lang:"))
async def cb_lang(callback: CallbackQuery, state: FSMContext) -> None:
    lang = callback.data.split(":")[1]
    await state.update_data(lang=lang)
    await state.set_state(InquiryForm.name)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(get_text("ask_name", lang))
    await callback.answer()


@router.message(InquiryForm.name)
async def step_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.update_data(name=message.text)
    await state.set_state(InquiryForm.phone)
    await message.answer(get_text("ask_phone", data["lang"]))


@router.message(InquiryForm.phone)
async def step_phone(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.update_data(phone=message.text)
    await state.set_state(InquiryForm.service)
    await message.answer(get_text("ask_service", data["lang"]), reply_markup=_service_keyboard(data["lang"]))


@router.callback_query(InquiryForm.service, F.data.startswith("service:"))
async def cb_service(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data["lang"]
    service_key = callback.data.split(":")[1]
    service_label = get_text(f"service_{service_key}", lang)
    await state.update_data(service=service_label)
    await state.set_state(InquiryForm.message)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(get_text("ask_message", lang))
    await callback.answer()


@router.message(InquiryForm.message)
async def step_message(message: Message, state: FSMContext, bot=None) -> None:
    data = await state.get_data()
    lang = data["lang"]
    lead = {
        "name":    data["name"],
        "phone":   data["phone"],
        "service": data["service"],
        "message": message.text,
        "lang":    lang,
    }

    await save_lead(**lead)

    await message.answer(get_text("thank_you", lang))

    summary = get_text("lead_summary", lang).format(**lead)
    try:
        await message.bot.send_message(ADMIN_CHAT_ID, summary)
    except Exception:
        logger.exception("Failed to notify admin")

    await state.clear()
