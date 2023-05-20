from aiogram.dispatcher.filters.state import StatesGroup, State


class GetMovie(StatesGroup):
    movie = State()
    name = State()
    description = State()
