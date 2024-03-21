from aiogram.fsm.state import StatesGroup, State


class WorkSpace(StatesGroup):
    upload_data = State()
    choose_file_type = State()
