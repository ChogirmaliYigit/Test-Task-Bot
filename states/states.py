from aiogram.dispatcher.filters.state import State, StatesGroup


class AllStates(StatesGroup):
    groups_list = State()
    fields = State()
    send_link = State()
    link = State()
