from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

workspaces = {
    'Выбрать РО': 'select_workspace',
    'Создать РО': 'create_workspace'
}

options = {
    'Умножение ✖️': 'multiple_data',
    'Сложение ➕': 'sum_data',
    'Вычитание ➖': 'diff_data',
    'Целая часть ➗': 'divide_data',
    'Остаток от деления ⁒': 'divide_diff_data',
    'Экспортировать РО ⏚': 'export_workspace',
}

export_types = {
    'CSV ': 'csv_export',
    'EXCEL': 'xlsx_export'
}


def create_workspace_options_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for option, callback in workspaces.items():
        builder.row(types.InlineKeyboardButton(
            text=option,
            callback_data=callback
        ))
    return builder.as_markup()


workspace_option_keyboard = create_workspace_options_keyboard()


def create_workspace_select_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="workspace",
        callback_data="workspace"
    ))
    return builder.as_markup()


workspace_button = create_workspace_select_button()

create_workspace_button = InlineKeyboardBuilder().add(types.InlineKeyboardButton(
    text="Создать РО",
    callback_data='create_workspace'
)).as_markup()


def select_option_to_work_with_data() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for option, callback in options.items():
        builder.row(types.InlineKeyboardButton(
            text=option,
            callback_data=callback
        ))
    return builder.as_markup()


options_with_data_keyboard = select_option_to_work_with_data()


def export_types_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for ex_type, callback in export_types.items():
        builder.row(types.InlineKeyboardButton(
            text=ex_type,
            callback_data=callback
        ))
    return builder.as_markup()


export_types_keyboard = export_types_builder()
