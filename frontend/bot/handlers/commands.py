from aiogram import Router, F

from aiogram.filters import Command
from aiogram.types import Message

from frontend.bot.utils.texts import START_TEXT
from frontend.bot.keyboards.inline_keyboards import workspace_option_keyboard

router = Router(name=__name__)


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(START_TEXT, reply_markup=workspace_option_keyboard)
