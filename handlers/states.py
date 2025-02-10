from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    waiting_for_option = State()
    waiting_for_document = State()
