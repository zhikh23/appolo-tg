from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    find__start = State()
    find__wait_id = State()
    find__wait_name = State()
    find__wait_tags = State()
