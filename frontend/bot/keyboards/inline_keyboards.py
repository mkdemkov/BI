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
