from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
position = CallbackData('ikb','action')
movie_callback = CallbackData('ikb2','id')
def mybutton(data:list,action=None):
    btn =InlineKeyboardMarkup(row_width=5)
    for count,film in enumerate(data,start=1):
        button = InlineKeyboardButton(text=f"{count}",callback_data=movie_callback.new(id=film['id']))
        btn.insert(button)
    btn.row(
        InlineKeyboardButton(text="⬅️",callback_data=position.new(action='back')),
        InlineKeyboardButton(text="❌", callback_data='cancel'),
        InlineKeyboardButton(text="➡️",callback_data=position.new(action='go'))

    )
    return btn
language_callback = CallbackData('ikb3','language')
btn = InlineKeyboardMarkup()
btn.add(InlineKeyboardButton(text="🇺🇿 O'zbek tili",callback_data=language_callback.new(language='uz')))
btn.add(InlineKeyboardButton(text="🇷🇺 Pусский язык",callback_data=language_callback.new(language='ru')))
btn.add(InlineKeyboardButton(text="🇬🇧 English",callback_data=language_callback.new(language='en')))


