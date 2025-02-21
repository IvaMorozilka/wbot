from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import BaseStorage


class States(StatesGroup):
    waiting_for_option = State()
    waiting_for_document = State()

    form_auth_key = State()
    form_full_name = State()
    form_org_name = State()
    check_state = State()
