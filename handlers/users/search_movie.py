from loader import dp,bot
from aiogram import types
from api import *
from aiogram.dispatcher import FSMContext
from keyboards.inline.buttons import *
@dp.message_handler(content_types='text')
async def get_movies_by_search(message:types.Message,state:FSMContext):
    language = get_user(telegram_id=message.from_user.id)
    search = search_movie(message.text)
    if search['results'] == []:
        if language=='uz':
            await message.answer("Afsuski u nom bilan kino topilmadi!")
        elif language=='ru':
            await message.answer("К сожалению, фильм с таким названием не найден!")
        else:
            await message.answer("Unfortunately, no movie was found with that name!")

    else:
        data  = search['results']
        await state.update_data({
            'data':data,
            'position':0,
            'count':len(data)
        })
        data = data[:5]
        if language=='uz':
            text = f"Natijalar: 1-5 dan {len(search['results'])}\n\n"
            for count, i in enumerate(data, start=1):
                text += f"{count}.{i['name']}\n"
            await message.answer(text,reply_markup=mybutton(data=data))
        elif language=='ru':
            text = f"Pезультаты: 1-5 из {len(search['results'])}\n\n"
            for count, i in enumerate(data, start=1):
                text += f"{count}.{i['name']}\n"
            await message.answer(text, reply_markup=mybutton(data=data))
        else:
            text = f"Results: 1-5 from {len(search['results'])}\n\n"
            for count, i in enumerate(data, start=1):
                text += f"{count}.{i['name']}\n"
            await message.answer(text, reply_markup=mybutton(data=data))

@dp.callback_query_handler(position.filter())
async def test(call:types.CallbackQuery,callback_data:dict,state:FSMContext):
    data = await state.get_data()
    action = callback_data['action']
    language = get_user(telegram_id=call.from_user.id)
    if action=='back':
        if data['position']==0:
            if language=='uz':
                await call.answer("Siz allaqachon birinchi sahifadasz!")
            elif language=='ru':
                await call.answer("Вы уже на первой странице!")
            else:
               await call.answer("You are already on the first page!")
        else:
            start = (data['position'] -1)
            finish = data['position']
            info = data['data']
            datas = info[start*5:finish*5]
            if datas:
                if language == 'uz':
                    text = f"Natijalar: {1 if start*5==0 else start*5}-{finish * 5} dan {data['count']}\n\n"
                    for count, i in enumerate(datas, start=1):
                        text += f"{count}.{i['name']}\n"
                    await call.message.edit_text(text, reply_markup=mybutton(data=datas))
                elif language == 'ru':
                    text = f"Pезультаты: {1 if start*5==0 else start*5}-{finish * 5} из {data['count']}\n\n"
                    for count, i in enumerate(datas, start=1):
                        text += f"{count}.{i['name']}\n"
                    await call.message.edit_text(text, reply_markup=mybutton(data=datas))
                else:
                    text = f"Results: {1 if start*5==0 else start*5}-{finish * 5} from {data['count']}\n\n"
                    for count, i in enumerate(datas, start=1):
                        text += f"{count}.{i['name']}\n"
                    await call.message.edit_text(text, reply_markup=mybutton(data=datas))
                await state.update_data({
                    'position': start
                })
            else:
                if language == 'uz':
                    await call.answer("Malumot topilmadi!")
                elif language == 'ru':
                    await call.answer("Информация не найдена!")
                else:
                    await call.answer("Not found data!")
    if action=='go':
            start =(data['position']+1)
            finish = (data['position']+2)
            info = data['data']
            datas = info[start*5:finish*5]
            if datas:
                if language == 'uz':
                    text = f"Natijalar: {start * 5}-{finish * 5} dan {data['count']}\n\n"
                    for count, i in enumerate(datas, start=1):
                        text += f"{count}.{i['name']}\n"
                    await call.message.edit_text(text, reply_markup=mybutton(data=datas))
                elif language == 'ru':
                    text = f"Pезультаты: {1 if start * 5 == 0 else start * 5}-{finish * 5} из {data['count']}\n\n"
                    for count, i in enumerate(datas, start=1):
                        text += f"{count}.{i['name']}\n"
                    await call.message.edit_text(text, reply_markup=mybutton(data=datas))
                else:
                    text = f"Results: {1 if start * 5 == 0 else start * 5}-{finish * 5} from {data['count']}\n\n"
                    for count, i in enumerate(datas, start=1):
                        text += f"{count}.{i['name']}\n"
                    await call.message.edit_text(text, reply_markup=mybutton(data=datas))
                await state.update_data({
                    'position': start
                })
            else:
                if language == 'uz':
                    await call.answer("Malumot topilmadi!")
                elif language == 'ru':
                    await call.answer("Информация не найдена!")
                else:
                    await call.answer("Not found data!")

@dp.callback_query_handler(movie_callback.filter())
async def get_movie(call:types.CallbackQuery,callback_data:dict):
    id  = callback_data['id']
    await call.answer(cache_time=60)
    movie = get_film(id)
    language = get_user(telegram_id=call.from_user.id)
    if movie=='Ok':
        if language=='uz':
            await call.message.answer("Uzur bu film topilmadi!")
        elif language=='ru':
            await call.message.answer("К сожалению, этот фильм не найден!")
        else:
            await call.message.answer("Sorry, this movie was not found!")
        await call.message.delete()
    else:
        try:
            if language == 'uz':
                await call.message.answer_document(document=movie['file_id'],
                                                   caption=f"Kino nomi: <b>{movie['name']}</b>\n"
                                                           f"Kino haqida:👇👇👇\n"
                                                           f"{movie['description']}")
            elif language == 'en':
                await call.message.answer_document(document=movie['file_id'],
                                                   caption=f"Movie name: <b>{movie['name']}</b>\n"
                                                           f"About the movie:👇👇👇\n"
                                                           f"{movie['description']}")
            else:
                await call.message.answer_document(document=movie['file_id'],
                                                   caption=f"Название фильма: <b>{movie['name']}</b>\n"
                                                           f"О фильме:👇👇👇\n"
                                                           f"{movie['description']}")
            await call.message.delete()
        except Exception as e:
            if language == 'uz':
                await call.message.answer("Uzur bu film topilmadi!")
            elif language == 'ru':
                await call.message.answer("К сожалению, этот фильм не найден!")
            else:
                await call.message.answer("Sorry, this movie was not found!")
            await call.message.delete()
@dp.callback_query_handler(text='cancel')
async def cancel_button(call:types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()



