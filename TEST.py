import logging
from aiogram import Bot, executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from gspread import WorksheetNotFound
import keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import gspread
import time
import random

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
    await message.reply("В разработке", reply_markup=kb.keyboard_back)


@dp.message_handler(text="Забронировать книгу")
async def process_help_command(message: types.Message):
    await message.reply("Введите название книги", reply_markup=kb.keyboard_back)
    await St.bookbron.set()


@dp.message_handler(text="Назад", state='*')
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
                            reply_markup=kb.keyboard_back_and_otz)
                    else:
                        print("Название библиотеки не коректное")
            else:
                print("не найдено")
    if b2 == 0:
        await message.reply("такой книги нет", reply_markup=kb.keyboard_back)
    await state.finish()





@dp.message_handler(text="отз")
async def otz(message: types.Message, state: FSMContext):
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
            if aid == user_id and bron == ne_bron : # сравниваем и если не пустата то отсылаем юзеру который в табл сообщение о просьбе оставить отзыв
                print( aid)
                await message.answer(f"вы недавно прочитали книгу '{cv}', не хотите ли оставить отзыв?", reply_markup=kb.key_otz)


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
            texts = message.text
            bron = nekniga['бронь']
            ne_bron = "не забронировано"
            if bron == ne_bron and aid == user_id:
                lost = [cv, texts, user_id]
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
            texts = message.text.lower()
            await message.reply(texts)
            otz = nekniga['отзыв']
            if aid != '' and cv == texts:
                await message.answer(f"отзыв о книге{cv}:\n {otz}\n его написал пользователь с id{aid}")



@dp.message_handler(text="Оставить отзыв")
async def process_help_command(msg: types.Message, state: FSMContext):
    await msg.answer("Введите отзыв")
    texts = msg.text
    id = msg.chat.id
    lost = {id: texts}

    worksheet2.append_row(lost)






if __name__ == '__main__':
    worksheet_biblioteki = gsheets()
    worksheet_poisk = knigi()
    executor.start_polling(dp, skip_updates=True)

# TODO ээээ..... потом кароч доделаю(система отзывов книг)





@dp.message_handler(text="введите отзыв")
async def process_help_command(msg: types.Message, state: FSMContext):
    texts = await state.get_data()
    texts = msg.text
    await msg.answer("осталось только отправить", reply_markup=kb.key_otz)



@dp.message_handler(text="отправить")
async def process_help_command(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    print("-----")
    # lost = {data: texts}
    # print(lost)
    # worksheet2.append_row(lost)


