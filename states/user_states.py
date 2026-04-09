from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_category = State()
    waiting_for_question = State()
