from aiogram.fsm.state import StatesGroup, State


class Operation(StatesGroup):
    set_operand = State()
    set_column = State()
