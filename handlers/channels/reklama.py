from loader import dp,bot
from aiogram import types
from api import get_users
from data.config import REKLAMA_KANAL
import asyncio
# Send Post to Bot Members
@dp.channel_post_handler(content_types='any')
async def send_users(message:types.Message):
    message_id = message.message_id
    from_chat_id = REKLAMA_KANAL
    for i in get_users():
        try:
            await bot.forward_message(chat_id=i['telegram_id'],from_chat_id=from_chat_id,message_id=message_id)
            await asyncio.sleep(1)
        except:
            pass