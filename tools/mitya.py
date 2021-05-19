from gspread.exceptions import WorksheetNotFound
from misc import worksheet1, sh
from aiogram.dispatcher.filters.state import StatesGroup, State
from misc import profil, knigi_polzovately
import random
import time


# Функция скачивания скачивания и сохранения библиотек
def gsheets():
    for i in worksheet1:
        try:
            print(worksheet1)
            return worksheet1
        except WorksheetNotFound:
            print(f'!!! -> Страница "{i["название"]}" не найдена <- !!!')


# Функция скачивания скачивания и сохранения книг
def knigi():
    dict = {}
    a = 0
    for e in gsheets():
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
        except WorksheetNotFound:
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


def profile():
    for i in profil:
        try:
            print(profil)
            return profil
        except WorksheetNotFound:
            print(f'!!! -> Страница "{i["название"]}" не найдена <- !!!')


def knigi_and_id_polzovately():
    for i in profil:
        try:
            print(knigi_polzovately)
            return knigi_polzovately
        except WorksheetNotFound:
            print(f'!!! -> Страница "{i["название"]}" не найдена <- !!!')


# Состояния
class St(StatesGroup):
    book0 = State()  # Поиск книги
    book = State()  # Поиск книги
    bookbron = State()  # Бронь книги
    bookbron1 = State()  # Бронь книги
    text1 = State()
    texts = State()
    pross = State()
    pross = State()
    otz = State()
    spotz = State()
    addotz = State()


worksheet_biblioteki = gsheets()
worksheet_poisk = knigi()
worksheet_profile = profile()
worksheet_o_knigax = knigi_and_id_polzovately()