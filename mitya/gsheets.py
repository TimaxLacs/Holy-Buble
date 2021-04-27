import random
from asyncio import run_coroutine_threadsafe, get_event_loop, new_event_loop, sleep

import gspread
import time


na_time = time.strftime('%M')
gc = gspread.service_account()
sh = gc.open("holy buble")
worksheet1 = sh.worksheet_biblioteki("Библиотека").get_all_records()

dict = {}

worksheet_knigi = {}
worksheet = "324242"

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
    return dict




#print(worksheet_knigi)

if __name__ == '__main__':
    run_coroutine_threadsafe(gsheets())


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


