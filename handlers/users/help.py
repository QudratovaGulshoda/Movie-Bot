from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")
    
    await message.answer_document(document="BQACAgIAAxkBAANGZGOdHkN-uRHanw0XiTspdb8-jRQAAr0vAAKDxBFLJ_HpaThtW44vBA")