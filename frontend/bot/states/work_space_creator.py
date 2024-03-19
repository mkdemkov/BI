from aiogram.fsm.state import StatesGroup, State


class WorkSpaceCreator(StatesGroup):
    set_name = State()
    upload_data = State()