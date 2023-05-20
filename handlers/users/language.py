from loader import dp,bot
from aiogram import types
from api import *
from keyboards.inline.buttons import *
@dp.message_handler(commands='set_language')
async def change(message:types.Message):
    language  = get_user(telegram_id=message.from_user.id)
    if language=='uz':
        await message.answer("Kerakli tilni tanlang.",reply_markup=btn)
    elif language=='ru':
        await message.answer("Выберите нужный язык.",reply_markup=btn)
    else:
        await message.answer("Choose language.",reply_markup=btn)
@dp.callback_query_handler(language_callback.filter())
async def change_language(call:types.CallbackQuery,callback_data:dict):
    language = callback_data['language']
    change_language_bot(telegram_id=call.from_user.id,language=language)
    if language=='uz':
        await call.answer("Yangi til sozlandi!")
    elif language == 'ru':
        await call.answer("Настроен новый язык!")
    else:
        await call.answer("Language accepted!")
    await call.message.delete()


