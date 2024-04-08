import os
import time

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from frontend.bot.main import bot
from frontend.bot.misc.export import process_csv_export, process_excel_export
from frontend.bot.misc.import_data import form_data_csv, form_data_excel
from frontend.bot.states.operation import Operation
from frontend.bot.states.work_space import WorkSpace
from frontend.bot.keyboards.inline_keyboards import create_workspace_button, options_with_data_keyboard, \
    export_types_keyboard
from frontend.bot.get_info_from_api import get_workspace, import_data, transform_data
from frontend.bot.utils.tuples import show_tuples

router = Router(name=__name__)

oper = None
num = None
col = None


@router.callback_query(F.data == "select_workspace")
async def select_workspace_option(callback: types.CallbackQuery):
    response = await get_workspace()
    if not response:
        await callback.message.edit_text("РО не найдена ⛔️\nСоздайте новую РО", reply_markup=create_workspace_button)
    else:
        tuples = response[0]
        tuples_to_show = show_tuples(tuples)
        await callback.message.edit_text(tuples_to_show, reply_markup=options_with_data_keyboard)  # add reply markup


@router.callback_query(F.data == "create_workspace")
async def create_workspace_option(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(WorkSpace.upload_data)
    await callback.message.answer("Отправьте <b>CSV</b> или <b>XLSX(Excel)</b> файл")


@router.message(WorkSpace.upload_data)
async def file_test(message: types.Message, state: FSMContext):
    if not message.document:
        await message.answer("Отправьте <b>CSV</b> или <b>XLSX(Excel)</b> файл")
        return
    if not (message.document.file_name.endswith(".csv") or message.document.file_name.endswith(".xlsx")):
        await message.answer("Поддерживаемые форматы: <b>CSV</b> и <b>XLSX</b>\n\nОтправьте нужный файл повторно")
        return
    filename = message.document.file_name
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    destination_file = os.path.join(parent_dir, "user_data", message.document.file_name)
    await bot.download_file(file_path, destination=destination_file)
    message = \
        await message.answer(
            f"Файл {filename} загружен, РО добавлена ✅\nПодождите, сейчас данные загрузятся и с ними можно будет работать"
        )
    if filename.endswith('csv'):
        data = form_data_csv(destination_file)
    else:
        data = form_data_excel(destination_file)
    res = await import_data(data)
    res = res[0]
    tuples_to_show = show_tuples(res)
    await message.answer(tuples_to_show, reply_markup=options_with_data_keyboard)
    await state.clear()


@router.callback_query(F.data == 'multiple_data')
async def multiply_data(callback: types.CallbackQuery, state: FSMContext):
    global oper
    oper = 'Умножение'
    await callback.message.answer("Укажите операнд <i>(целое число)</i>")
    await state.set_state(Operation.set_operand)


@router.callback_query(F.data == 'sum_data')
async def sum_data(callback: types.CallbackQuery, state: FSMContext):
    global oper
    oper = 'Сложение'
    await callback.message.answer("Укажите операнд <i>(целое число)</i>")
    await state.set_state(Operation.set_operand)


@router.callback_query(F.data == 'diff_data')
async def diff_data(callback: types.CallbackQuery, state: FSMContext):
    global oper
    oper = 'Вычитание'
    await callback.message.answer("Укажите операнд <i>(целое число)</i>")
    await state.set_state(Operation.set_operand)


@router.callback_query(F.data == 'divide_data')
async def divide_data(callback: types.CallbackQuery, state: FSMContext):
    global oper
    oper = 'Целая часть'
    await callback.message.answer("Укажите операнд <i>(целое число)</i>")
    await state.set_state(Operation.set_operand)


@router.callback_query(F.data == 'divide_diff_data')
async def divide_diff_data(callback: types.CallbackQuery, state: FSMContext):
    global oper
    oper = 'Остаток от деления'
    await callback.message.answer("Укажите операнд <i>(целое число)</i>")
    await state.set_state(Operation.set_operand)


@router.message(Operation.set_operand)
async def check_operand(message: types.Message, state: FSMContext):
    global num
    try:
        num = int(message.text)
        await message.answer("Укажите номер столбца <i>(нумерация с нуля)</i>)")
        await state.set_state(Operation.set_column)
    # не целое число в качестве операнда
    except ValueError:
        await message.answer("Недопустимый операнд ⛔️ \nПоддерживаются целые числа. Повторите ввод")
        return


@router.message(Operation.set_column)
async def check_column(message: types.Message, state: FSMContext):
    global col
    try:
        col = int(message.text)
        if col < 0:
            await message.answer("Недопустимый номер столбца ⛔️\nУкажите целое положительное число (или 0)")
            return
        await message.answer(
            f"Начал преобразование\nТип операции: <b>{oper}</b>\nОперанд: <b>{num}</b>\nСтолбец: <b>{col}</b>")
        res = await transform_data(oper, num, col)
        res = res[0]
        tuples_to_show = show_tuples(res)
        await message.answer(tuples_to_show, reply_markup=options_with_data_keyboard)
        await state.clear()

    except ValueError:
        await message.answer("Недопустимый номер столбца ⛔️\nУкажите целое положительное число (или 0)")
        return


@router.callback_query(F.data == 'export_workspace')
async def export_workspace(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите тип файла для экспорта", reply_markup=export_types_keyboard)
    await state.set_state(WorkSpace.choose_file_type)


@router.callback_query(F.data == 'csv_export')
async def export_csv(callback: types.CallbackQuery):
    await callback.message.answer("Начал экспорт ⌛️")
    await process_csv_export()
    time.sleep(0)  # заглушка чтобы файл точно обновился до отправки
    document = FSInputFile('data.csv')
    await callback.message.answer_document(document)


@router.callback_query(F.data == 'xlsx_export')
async def export_excel(callback: types.CallbackQuery):
    message = await callback.message.answer("Начал экспорт ⌛️")
    await process_excel_export()
    time.sleep(0)
    document = FSInputFile('data.xlsx')
    await callback.message.answer_document(document, caption="Результат экспорта ⬆️")
    await message.delete()
