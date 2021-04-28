import logging
from aiogram import Bot, executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import gspread
import time
import random

logging.basicConfig(level=logging.INFO)
bot = Bot(token="1703652201:AAGit3dd0CH4ZgYlWYW-OSRQskn5lTtkeRc")
dp = Dispatcher(bot, storage=MemoryStorage())
na_time = time.strftime('%M')
gc = gspread.service_account()
sh = gc.open("holy buble")
worksheet1 = sh.worksheet("Библиотека").get_all_records()


# Состояния
class St(StatesGroup):
    book0 = State()  # Поиск книги
    book = State()  # Поиск книги
    bookbron = State()  # Бронь книги
    bookbron1 = State()  # Бронь книги


def gsheets():
    for i in worksheet1:
        try:
            worksheet = sh.worksheet("Библиотека").get_all_records()
            print(worksheet)
            return worksheet
        except gspread.exceptions.WorksheetNotFound:
            print(f'!!! -> Страница "{i["название"]}" не найдена <- !!!')


def knigi():
    dict = {}
    a = 0
    for i in worksheet_biblioteki:
        if a > 10:
            continue
        a = a + 1
        try:
            print(f'--> Обрабатываю {i["название"]}')
            worksheet_knigi = sh.worksheet(i["название"]).get_all_records()
            if worksheet_knigi != []:
                kniga = [(i["название"], worksheet_knigi), ]
                dict.update(kniga)
                print(kniga)
            else:
                print('!!! -> Лист пуст <- !!!')
        except gspread.exceptions.WorksheetNotFound:
            print(f'!!! -> Лист "{i["название"]}" не найден <- !!!')
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
    await message.reply("выполнено", reply_markup=kb.keyboard_back)


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
    print(data)
    text = data['book']
    text1 = text.lower()
    shot_rast = 99999999999999999999999999999999999999
    adress = "Не найдено"
    biblioteka = "Не найдено"
    b2 = 0
    d = {}
    nalich = "есть в наличии"
    for sd in worksheet_poisk:
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for kniga in spisok_knig:
            print(spisok_knig)
            print(kniga)
            cv = kniga['книга']
            print(spisok_knig)
            if cv.lower() == text1 and nalich == kniga['наличие']:
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
                print("не найдено")
    if b2 == 0:
        await message.reply("такой книги нет", reply_markup=kb.keyboard_back)
    await state.finish()


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=St.bookbron1)
async def process_book_name(message: types.Message, state: FSMContext):
    await message.reply("Обрабатываю")  #
    data = await state.get_data()
    print(data)
    text = data['book1']
    text1 = text.lower()
    shot_rast = 99999999999999999999999999999999999999
    adress = "Не найдено"
    biblioteka = "Не найдено"
    bronurovanie = "забронировано"
    nalichie = "есть в наличии"
    nevnalichie = "нету в наличии"
    b2 = 0
    nebron = 'не забобронировано'
    for nz in worksheet_poisk:
        nazvanie_biblioteki = nz
        spisok_knig = worksheet_poisk[nazvanie_biblioteki]
        for kn in spisok_knig:
            kniga = kn['книга']
            bron = kn['бронь']
            nalich = kn['наличие']
            if kniga.lower() == text1 and nalich == nalichie and bron == nebron:
                for bibliotek in worksheet_biblioteki:
                    nazvanie = bibliotek['название']
                    if nazvanie_biblioteki == nazvanie:
                        print('Книга найдена!')
                        b2 = 1
                        f = bibliotek["кординаты"].split(", ")
                        rast = quick_distance(message.location.latitude, message.location.longitude, float(f[0]),
                                              float(f[1]))  # Вычисление растояния до библиотеке.
                        if rast < shot_rast:
                            shot_rast = rast
                            adress = bibliotek["адрес"]
                        await message.answer(
                            f'В библиотеки по этому адресу мы нужную вам книгу: {adress}.\n Название библиотеки: {nazvanie_biblioteki}.\n Вот растояние до этой библиотеки: {shot_rast}.',
                            reply_markup=kb.keyboard_back)
            else:
                print("Книга не подходит")
    if b2 == 0:
        await message.reply("такой книги нет", reply_markup=kb.keyboard_back)
    await state.finish()


if __name__ == '__main__':
    worksheet_biblioteki = gsheets()
    worksheet_poisk = knigi()
    executor.start_polling(dp, skip_updates=True)
