from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

workspaces = {
    'Выбрать РО': 'select_workspace',
    'Создать РО': 'create_workspace'
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
