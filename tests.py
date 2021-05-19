import logging
from aiogram import Bot, executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import gspread
import time
from datetime import datetime
import random
import re

logging.basicConfig(level=logging.INFO)
bot = Bot(token="1255862313:AAFWPZqLgPlHH-SXkfji79nLshUjp_SqwDk")
dp = Dispatcher(bot, storage=MemoryStorage())
na_time = time.strftime('%M')
gc = gspread.service_account()
sh = gc.open("holy buble")
worksheet1 = sh.worksheet("nazvanie").get_all_records()

worksheet2 = sh.worksheet("отзывы")

# Состояния
class St(StatesGroup):
    book0 = State()  # Поиск книги
    book = State()  # Поиск книги
    bookbron = State()  # Бронь книги
    bookbron1 = State()  # Бронь книги
    text1 = State()
    texts = State()
    pross = State()
    otz = State()
    spotz = State()
    addotz = State()




def gsheets():
    for i in worksheet1:
        try:
            print(worksheet1)
            return worksheet1
        except gspread.exceptions.WorksheetNotFound:
            print(f'!!! -> Страница "{i["название"]}" не найдена <- !!!')


def knigi():
    dict = {}
    a = 0
    for e in worksheet_biblioteki:
        a = a + 1
        if a >= 10:
            continue
        try:
            print(f'--> Обрабатываю {e["название"]}')
            worksheet_knigi = sh.worksheet(e["название"]).get_all_records()
            if worksheet_knigi != []:
                kniga = [(e["название"], worksheet_knigi), ]
                dict.update(kniga)
            else:
                print('!!! -> Лист пуст <- !!!')
        except gspread.exceptions.WorksheetNotFound:
            print(f'!!! -> Лист "{e["название"]}" не найден <- !!!')
        time.sleep(random.randint(2, 3))
    print(dict)
    return dict


# Быстрый расчет расстояния между двумя точками, низкая точность
def quick_distance(lat1, lng1, lat2, lng2):
    from math import cos, sqrt
    x = lat2 - lat1
    y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
    return int((111.138 * sqrt(x * x + y * y)) * 1000)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    print(message.chat.id)
    await message.answer("я вас слушаю, хозяин", reply_markup=kb.keyboard_menu)




@dp.message_handler(text="Ближащая библиотека")
async def process_help_command(message: types.Message):
    await message.reply("Запрашиваем вашу геолакацию", reply_markup=kb.markup_request)


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def rppr(message: types.Message):
    shot_rast = 9999999999999999999999999999999999999999999999999999999999999999
    adress = "Не найдено"
    biblioteka = "Не найдено"
    location = (0, 0)
    for i in worksheet_biblioteki:
        f = (i["кординаты"].split(", "))
        rast = quick_distance(message.location.latitude, message.location.longitude, float(f[0]),
                              float(f[1]))  # Вычисление растояния до библиотеке.
        if rast < shot_rast:
            shot_rast = rast
            adress = i["адрес"]
            biblioteka = (i["название"])
            location = (float(f[0]), float(f[1]))
    await message.answer(f'{shot_rast} метров от вас до ближайшей библиотеки.\nНазвание библиотеки: {biblioteka}.',
                         reply_markup=kb.keyboard_menu)
    inline_btn_1 = InlineKeyboardButton("Проложить маршрут",
                                        url=f"https://maps.google.com?saddr=Current+Location&daddr={location}")
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    await message.answer(f'Вот её адрес: {adress}.', reply_markup=inline_kb1)


@dp.message_handler(text="Узнать о своих книгах")
async def process_help_command(message: types.Message):
    await message.reply("выполнено", reply_markup=kb.keyboard_back)


@dp.message_handler(text="Оставить отзыв о книге")
async def process_help_command(message: types.Message):
    await message.reply("ввидите название книги к которой вы хотите оставить отзыв", reply_markup=kb.keyboard_back)
    await St.addotz.set()






@dp.message_handler(text="Забронировать книгу")
async def process_help_command(message: types.Message):
    await message.reply("Введите название книги", reply_markup=kb.keyboard_back)
    await St.bookbron.set()


@dp.message_handler(text="Назад", state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    print(message.chat.id)
    await message.answer("Вы вернулись на главную страницу", reply_markup=kb.keyboard_menu)
    await state.finish()

@dp.message_handler(text="Нет", state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    print(message.chat.id)
    await message.answer("Вы вернулись на главную страницу", reply_markup=kb.keyboard_menu)
    await state.finish()

@dp.message_handler(text="Профиль")
async def process_help_command(message: types.Message):
    await message.answer("Ваш профиль.\n Ваш уровень: ...\n Ваш опыт: ...\n Ваше количество баллов:... ",
                         reply_markup=kb.keyboard_back)


@dp.message_handler(text="Найти книгу")
async def process_help_command(message: types.Message):
    await message.reply("Введите название книги", reply_markup=kb.keyboard_back)
    await St.book0.set()


@dp.message_handler(state=St.book0)
async def process_book_name(message: types.Message, state: FSMContext):
    await message.reply(f"Запрошеная книга: {message.text}\nОтправте свое местоположение, чтобы мы нашли ближайшую "
                        f"библиотеку с этой книгой", reply_markup=kb.markup_request)
    await St.book.set()
    await state.update_data(book=message.text)


@dp.message_handler(state=St.bookbron)
async def process_book_name(message: types.Message, state: FSMContext):
    await message.reply(f"Запрошеная книга: {message.text}\nОтправте свое местоположение, чтобы мы нашли ближайшую и "
                        f"забронировали нужную вам книгу ", reply_markup=kb.markup_request)
    await St.bookbron1.set()
    await state.update_data(book1=message.text)


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=St.book)
async def process_book_name(message: types.Message, state: FSMContext):
    await message.reply("Обрабатываю")
    data = await state.get_data()
    print(data['book'])
    text = data['book']
    text1 = text.lower()
    shot_rast = 99999999999999999999999999999999999999
    adress = "Не найдено"
    biblioteka = "Не найдено"
    print("----=", text1)
    b2 = 0
    d = {}
    for sd in worksheet_poisk:
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for kniga in spisok_knig:
            cv = kniga['книга']
            if cv.lower() == text1:
                for i in worksheet_biblioteki:
                    nazvanie = i["название"]
                    if nazvanie == sd:
                        print('Книга числится в библиотеке')
                        b2 = 1
                        f = (i["кординаты"].split(", "))
                        rast = quick_distance(message.location.latitude, message.location.longitude, float(f[0]),
                                              float(f[1]))  # Вычисление растояния до библиотеке.
                        if rast < shot_rast:
                            shot_rast = rast
                            adress = i["адрес"]
                            biblioteka = (i["название"])
                        await message.answer(
                            f'В библиотеки по этому адресу есть нужная вам книга: {adress}.\n Название библиотеки: {biblioteka}.\n Вот растояние до этой библиотеки: {shot_rast}.',
                            reply_markup=kb.keyboard_back)
                    else:
                        print("Название библиотеки не коректное")
            else:
                print("не найдено")
    if b2 == 0:
        await message.reply("такой книги нет", reply_markup=kb.keyboard_back)
    await state.finish()







@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 1:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                proza = 'проза'
                #print(cv)
                #print(zanr, "1111111")
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('проза')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)

                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    elif code == 2:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('фентези')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)
                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    elif code == 3:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('роман')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)
                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    elif code == 4:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('эротика')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)
                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    elif code == 5:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('детектив')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)
                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    else:
        await bot.answer_callback_query(callback_query.id)



@dp.message_handler(text="Поиск книги по жанру")
async def process_command_2(message: types.Message):
    await message.reply("выбирите жанр книги", reply_markup=kb.inline_kb_full)







@dp.message_handler(state=St.otz)
async def otz(message: types.Message, state: FSMContext):
    print("-------")
    for sd in worksheet_poisk:
        print(worksheet_poisk)
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for nekniga in spisok_knig:
            print("---------", nekniga)
            cv = nekniga['книга']
            print("-----------------", cv)
            aid = nekniga['айди']
            print(aid)
            user_id = message.chat.id
            bron = nekniga['бронь']
            ne_bron = "не забронировано"
            print(aid, bron)
            if aid == user_id and bron == ne_bron:  # сравниваем и если не пустата то отсылаем юзеру который в табл сообщение о просьбе оставить отзыв
                print(aid)
                await message.answer(f"вы недавно прочитали книгу '{cv}', не хотите ли оставить отзыв?",
                                             reply_markup=kb.keyboard_net_and_otz)
                time.sleep(10)




@dp.message_handler(text="Оставить отзыв")
async def process_help_command(message: types.Message, state: FSMContext):
    await message.answer("введите отзыв")
    await St.texts.set()



@dp.message_handler(state=St.texts)
async def process_help_command(message: types.Message, state: FSMContext):
    print("+++++++++++++++")
    for sd in worksheet_poisk:
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for nekniga in spisok_knig:
            cv = nekniga['книга']
            aid = nekniga['айди']
            user_id = message.chat.id
            textst = message.text
            bron = nekniga['бронь']
            ne_bron = "не забронировано"
            if bron == ne_bron and aid == user_id:
                lost = [cv, textst, user_id]
                worksheet2.append_row(lost)
                await message.answer("отзыв оставлен")
    await state.finish()




@dp.message_handler(text="Посмотреть отзовы")
async def process_help_command(message: types.Message, state: FSMContext):
    await message.answer("Отзывы к какой книге вы хотите посмотреть?")
    await St.pross.set()


@dp.message_handler(text=St.pross)
async def process_help_command(message: types.Message, state: FSMContext):
    for sd in worksheet_poisk:
        print(worksheet_poisk)
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for nekniga in spisok_knig:
            cv = nekniga['книга']
            aid = nekniga['айди']
            textst = message.text.lower()
            await message.reply(textst)
            otz = nekniga['отзыв']
            if aid != '' and cv == textst:
                await message.answer(f"отзыв о книге{cv}:\n {otz}\n его написал пользователь с id{aid}")



@dp.message_handler(text="Оставить отзыв")
async def process_help_command(msg: types.Message, state: FSMContext):
    await msg.answer("Введите отзыв")
    texts = msg.text
    idd = msg.chat.id
    lost = {idd: texts}
    worksheet2.append_row(lost)




@dp.message_handler()
async def otz(message: types.Message, state: FSMContext):
    print("+++++")
    await St.otz.set()
    print("=====")

if __name__ == '__main__':
    worksheet_biblioteki = gsheets()
    worksheet_poisk = knigi()
    executor.start_polling(dp, skip_updates=True)





def knigi():
    dict = {}
    a = 0
    time_now = datetime.now().strftime("%M")
    zero_time = 00
    if time_now == zero_time:
        for e in worksheet_biblioteki:
            a = a + 1
            if a >= 10:
                continue
            try:
                print(f'--> Обрабатываю {e["название"]}')
                worksheet_knigi = sh.worksheet(e["название"]).get_all_records()
                if worksheet_knigi != []:
                    kniga = [(e["название"], worksheet_knigi), ]
                    dict.update(kniga)
                else:
                    print('!!! -> Лист пуст <- !!!')
            except gspread.exceptions.WorksheetNotFound:
                print(f'!!! -> Лист "{e["название"]}" не найден <- !!!')
            time.sleep(random.randint(2, 3))
        print(dict)
        return dict



#TODO если в отзовах пусто,  то ничего не присылает

@dp.message_handler(state=St.otz)
async def otz(message: types.Message, state: FSMContext):
    print("-------")
    for sd in worksheet_poisk:
        print(worksheet_poisk)
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for nekniga in spisok_knig:
            print("---------", nekniga)
            cv = nekniga['книга']
            print("-----------------", cv)
            aid = nekniga['айди']
            print(aid)
            user_id = message.chat.id
            bron = nekniga['бронь']
            ne_bron = "не забронировано"
            print(aid, bron)
            if aid == user_id and bron == ne_bron:  # сравниваем и если не пустата то отсылаем юзеру который в табл сообщение о просьбе оставить отзыв
                print(aid)
                for o in worksheet2:
                    worksheet_otz = sh.worksheet(o['отзыв']).get_all_records()
                    worksheet_id =  sh.worksheet(o['айди']).get_all_records()
                    print("++++++++++++++", worksheet_otz, worksheet_id, "++++++++++++++")
                    if worksheet_id == user_id and worksheet_otz != ():
                        print(worksheet_otz, worksheet_id)
                        await message.answer(f"вы недавно прочитали книгу '{cv}', не хотите ли оставить отзыв?",
                                             reply_markup=kb.keyboard_net_and_otz)
                    else:
                        print("noooooooooo")



