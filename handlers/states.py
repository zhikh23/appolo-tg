from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    find__start = State()
    find__enter_id = State()
    find__enter_name = State()
    find__enter_tags = State()

    load__enter_type = State()
    load__enter_url = State()
    load__enter_file = State()
    load__enter_name = State()
    load__enter_description = State()
    load__enter_tags = State()
