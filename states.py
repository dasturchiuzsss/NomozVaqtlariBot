from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    language = State()
    phone_number = State()
    location = State()

