import logging
from aiogram import types
from data.config import CHANNELS
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from loader import bot, dp
from data.config import CHANNELS
from utils.misc import subscription
from api import *
@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    user = message.from_user.id
    final_status = True
    name = message.from_user.full_name
    create_user(name=name,telegram_id=user)
    language = get_user(telegram_id=message.from_user.id)
    btn = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        status = await subscription.check(user_id=user,
                                          channel=channel)
        final_status *= status
        channel = await bot.get_chat(channel)
        if status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
        if not status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
    if language == 'uz':
        btn.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs"))
    elif language == 'ru':
        btn.add(InlineKeyboardButton(text="Проверить подписку", callback_data="check_subs"))
    else:
        btn.add(InlineKeyboardButton(text="Check subscription", callback_data="check_subs"))
    if final_status:
        if language=='uz':
            await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n"
                             f"O'zingizga kerakli film nomini yozing!")
        elif language=='ru':
            await message.answer(f"Привет {message.from_user.full_name}!\n"
                                 f"Напишите название фильма сами!")
        else:
            await message.answer(f"Hello {message.from_user.full_name}!\n"
                                 f"Write your needs  movie title!")
    if not final_status:
        if language=='uz':
           await message.answer("Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling!", disable_web_page_preview=True, reply_markup=btn)
        elif language == 'ru':
            await message.answer("Подпишитесь на следующие каналы, чтобы использовать бота!",
                                 disable_web_page_preview=True, reply_markup=btn)
        else:
            await message.answer("Subscribe to the following channels to use the bot!!",
                                 disable_web_page_preview=True, reply_markup=btn)

@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    language = get_user(call.from_user.id)
    btn = InlineKeyboardMarkup()
    final_status = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        final_status *=status
        channel = await bot.get_chat(channel)
        if not status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
    if language=='uz':
       btn.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs"))
    elif language=='ru':
        btn.add(InlineKeyboardButton(text="Проверить подписку", callback_data="check_subs"))
    else:
        btn.add(InlineKeyboardButton(text="Check subscription", callback_data="check_subs"))
    if final_status:
        if language=='uz':
             await call.message.answer("Siz hamma kanalga a'zo bo'lgansiz!")
        elif language=='ru':
            await call.message.answer("Вы подписаны на все каналы!")
        else:
            await call.message.answer("You are subscribed to all channels!")
    if not final_status:
        await call.answer(cache_time=60)
        if language=='uz':
          await call.message.answer("Siz quyidagi kanal(lar)ga obuna bo'lmagansiz!",reply_markup=btn)
        elif language=='ru':
            await call.message.answer("Вы не подписаны на канал(ы) ниже!", reply_markup=btn)
        else:
            await call.message.answer("You are not subscribed to the channel(s) below!", reply_markup=btn)

        await call.message.delete()
