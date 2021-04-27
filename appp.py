import gspread
import time
import random
import keyboards as kb
from gspread import WorksheetNotFound


na_time = time.strftime('%M') # текущее время в минутах
gc = gspread.service_account()
sh = gc.open("holy buble")
worksheet1 = sh.worksheet("Библиотека").get_all_records() # заходим в лисит и берем значение в виде списка
worksheet2 = sh.worksheet("отзывы")



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
    for i in worksheet_biblioteki:
        print(i['название'])
        try:
            print(f'--> Обрабатываю {i["название"]}')
            worksheet_knigi = sh.worksheet(i["название"]).get_all_records()
            if worksheet_knigi != []:
                kniga = [(i["название"], worksheet_knigi), ]
                dict.update(kniga)
            else:
                print('!!! -> Лист пуст <- !!!')
        except gspread.exceptions.WorksheetNotFound:
            print(f'!!! -> Лист "{i["название"]}" не найден <- !!!')
        time.sleep(random.randint(2, 3))
    print(dict)
    return dict


def quick_distance(lat1, lng1, lat2, lng2):
    from math import cos, sqrt
    x = lat2 - lat1
    y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
    return int((111.138 * sqrt(x * x + y * y)) * 1000)


(commands="start")
def cmd_start(message: types.Message):
    print(message.chat.id)
    print("я вас слушаю, хозяин")

(text="Ближащая библиотека")
def process_help_command(message: types.Message):
    print("Запрашиваем вашу геолакацию")



(content_types=types.ContentTypes.LOCATION)
def rppr(message: types.Message):
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
    print(f'{shot_rast} метров от вас до ближайшей библиотеки.\nНазвание библиотеки: {biblioteka}.',
                         reply_markup=kb.keyboard_menu)
    inline_btn_1 = InlineKeyboardButton("Проложить маршрут",
                                        url=f"https://maps.google.com?saddr=Current+Location&daddr={location}")
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    print(f'Вот её адрес: {adress}.', reply_markup=inline_kb1)


def process_help_command(message: types.Message):
    await message.reply("выполнено", reply_markup=kb.keyboard_back)

