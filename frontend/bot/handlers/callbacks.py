from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from frontend.bot.states.work_space_creator import WorkSpaceCreator

router = Router(name=__name__)


@router.callback_query(F.data == "select_workspace")
async def select_workspace_option(callback: types.CallbackQuery):
    await callback.message.answer(f"Clicked {callback.data}")


@router.callback_query(F.data == "create_workspace")
async def create_workspace_option(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название РО")
    await state.set_state(WorkSpaceCreator.set_name)
