from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from frontend.bot.misc.export import process_csv_export
from frontend.bot.states.work_space import WorkSpace
from frontend.bot.keyboards.inline_keyboards import create_workspace_button, options_with_data_keyboard, \
    export_types_keyboard
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
        await callback.message.edit_text(tuples_to_show, reply_markup=options_with_data_keyboard)  # add reply markup


@router.callback_query(F.data == "create_workspace")
async def create_workspace_option(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(WorkSpace.upload_data)
    await callback.message.answer("Отправьте <b>CSV</b> файл с разделителем <b>;</b> или <b>XLSX(Excel)</b> файл")


@router.message(WorkSpace.upload_data)
async def file_test(message: types.Message, state: FSMContext):
    if not message.document:
        await message.answer("Отправьте <b>CSV</b> файл с разделителем <b>;</b> или <b>XLSX(Excel)</b> файл")
        return
    if not (message.document.file_name.endswith(".csv") or message.document.file_name.endswith(".xlsx")):
        await message.answer("Поддерживаемые форматы: <b>CSV</b> и <b>XLSX</b>\n\nОтправьте нужный файл повторно")
        return
    # Stop here
    await message.answer(message.document.file_name, reply_markup=options_with_data_keyboard)
    await state.clear()


@router.callback_query(F.data == 'export_workspace')
async def export_workspace(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите тип файла для эскпорта", reply_markup=export_types_keyboard)
    await state.set_state(WorkSpace.choose_file_type)
    # data = await load_data_and_export()  # all the tuples stored
    # print(data)


@router.callback_query(F.data == 'csv_export')
async def export_csv(callback: types.CallbackQuery):
    await process_csv_export()
    document = FSInputFile('data.csv')
    await callback.message.answer_document(document)


@router.callback_query(F.data == 'xlsx_export')
async def export_excel(callback: types.CallbackQuery):
    await callback.message.answer("excel")
