from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    unregistered = State()
    waiting_for_secret_phrase = State()
    waiting_for_surname = State()
    waiting_for_name = State()
    registered = State()
