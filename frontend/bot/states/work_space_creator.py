from aiogram.fsm.state import StatesGroup, State


class WorkSpaceCreator(StatesGroup):
    upload_data = State()
