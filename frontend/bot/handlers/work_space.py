from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from frontend.bot.states.work_space_creator import WorkSpaceCreator

router = Router(name=__name__)


@router.message(WorkSpaceCreator.set_name)
async def set_workspace_name(message: Message, state: FSMContext):
    await message.answer(f"You set name {message.text}")
