from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from frontend.bot.states.work_space_creator import WorkSpaceCreator
from frontend.bot.keyboards.inline_keyboards import create_workspace_button
from frontend.bot.get_info_from_api import get_workspace
from frontend.bot.utils.tuples import show_tuples, create_tuples

router = Router(name=__name__)


@router.callback_query(F.data == "select_workspace")
async def select_workspace_option(callback: types.CallbackQuery):
    response = await get_workspace()
    if not response:
        await callback.message.edit_text("РО не найдена! Создайте новую РО", reply_markup=create_workspace_button)
    else:
        tuples = response[0]
        tuples_to_show = show_tuples(tuples)
        await callback.message.edit_text(tuples_to_show)  # add reply markup


@router.callback_query(F.data == "create_workspace")
async def create_workspace_option(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(WorkSpaceCreator.upload_data)
    await callback.message.answer("Отправьте <b>CSV</b> файл с разделителем <b>;</b> или <b>XLSX(Excel)</b> файл")


@router.message(WorkSpaceCreator.upload_data)
async def file_test(message: types.Message, state: FSMContext):
    if not message.document:
        await message.answer("Отправьте <b>CSV</b> файл с разделителем <b>;</b> или <b>XLSX(Excel)</b> файл")
        return
    if not (message.document.file_name.endswith(".csv") or message.document.file_name.endswith(".xlsx")):
        await message.answer("Поддерживаемые форматы: <b>CSV</b> и <b>XLSX</b>\n\nОтправьте нужный файл повторно")
        return
    await message.answer(message.document.file_name)
    await state.clear()


@router.message()
async def other(message: types.Message):
    print(message.text)
