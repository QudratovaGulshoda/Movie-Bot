from loader import dp,bot
from aiogram import types
from data.config import KINOCHILAR
from states.MovieState import *
from aiogram.dispatcher import FSMContext
from api import *
@dp.message_handler(commands='write',chat_id=KINOCHILAR)
async def test(message:types.Message):
    language = get_user(telegram_id=message.from_user.id)
    if language=='uz':
       await message.answer("<b>Kino yuklashni boshlaymiz....\n</b>"
                         "<b>Kino videosi(mp4)ni yuboring</b>")
    elif language=='ru':
        await message.answer("<b>Начнем загружать фильм....\n</b>"
                             "<b>Отправить видеофильм (mp4).</b>")
    else:
        await message.answer("<b>Let's start downloading the movie....\n</b>"
                             "<b>Send movie video(mp4).</b>")

    await GetMovie.movie.set()
@dp.message_handler(content_types=['video','document'],state=GetMovie.movie)
async def test(message:types.Message,state:FSMContext):
      language = get_user(telegram_id=message.from_user.id)
      file_id = ''
      if message.content_type=='document':
          file_id = message.document.file_id
      else:
          file_id =message.video.file_id
      await state.update_data({
          'file_id':file_id
      })
      if language=='uz':
         await message.answer("<b>Kino nomini yuboring...\n</b>"
                           "<i>Masalan: Forsaj</i>")
      elif language=='en':
          await message.answer("<b>Submit movie title...\n</b>"
                               "<i>Example: Forsaj</i>")
      else:
          await message.answer("<b>Введите название фильма...\n</b>"
                               "<i>Пример: Forsaj</i>")
      await GetMovie.next()
@dp.message_handler(content_types='text',state=GetMovie.name)
async def test(message:types.Message,state:FSMContext):
    language = get_user(telegram_id=message.from_user.id)
    await state.update_data({
        'name':message.text
    })
    if language=='uz':
        await message.answer("<b>Kino haqida qisqacha yozing.\n</b>"
                         "<i>/skip (Agar shu qismini o'tkazib yuborsangiz)</i>")
    elif language=='ru':
        await message.answer("<b>Напишите небольшой рассказ о фильме.\n</b>"
                             "<i>/skip (Если вы пропустите эту часть)</i>")
    else:
        await message.answer("<b>Write a short story about the movie.\n</b>"
                             "<i>/skip (If you skip this part)</i>")

    await GetMovie.next()
@dp.message_handler(content_types='text',state=GetMovie.description)
async def test(message:types.Message,state:FSMContext):
    description = '' if message.text=='/skip' else message.text
    await state.update_data({
        'description':description
    })
    language = get_user(telegram_id=message.from_user.id)
    if language=='uz':
         await message.answer("Kino muvaffaqiyatli yuklandi!")
    elif language=='ru':
        await message.answer("Фильм успешно загружен!")
    else:
        await message.answer("Movie uploaded successfully!")
    data = await state.get_data()
    create_movie(name=data['name'],file_id=data['file_id'],description=description)
    await state.finish()
