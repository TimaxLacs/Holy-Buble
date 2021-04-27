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




("Ближащая библиотека")
def process_help_command(message: types.Message):
    print("Запрашиваем вашу геолакацию")



("вызываеться когда запрашиваем геолокацию ")
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
                         "тут кнопка меню ")
    inline_btn_1 = InlineKeyboardButton("Проложить маршрут",
                                        url=f"https://maps.google.com?saddr=Current+Location&daddr={location}")
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    print(f'Вот её адрес: {adress}.', "кнопка которая тут была больше нет так что пусть будет (кнопка назад)")

("Узнать о своих книгах")
def process_help_command(message: types.Message):
    print("выполнено","кнопка назад")





("Забронировать книгу")
def process_help_command(message: types.Message):
    print("Введите название книги", "кнопка назад")
    "вызываем St.bookbron.set()"

("Назад", )
def cmd_start(message: types.Message, state: FSMContext):
    print(message.chat.id)
    print("Вы вернулись на главную страницу", "кнопка отправить свою геолакацию")
    "конец state.finish() (отсылает в начало)"





("Найти книгу")
def process_help_command(message: types.Message):
    print("Введите название книги",  "кнопка назад")
    ("отсылаем к St.book0")

("St.book0")
def process_book_name(message: types.Message, state: FSMContext):
    print(f"Запрошеная книга: {message.text}\nОтправте свое местоположение, чтобы мы нашли ближайшую "
                        f"библиотеку с этой книгой", "кнопка отправить свою геолакацию")


@dp.message_handler(text="Забронировать книгу")
async def process_help_command(message: types.Message):
    await message.reply("Введите название книги", reply_markup=kb.keyboard_back)
    "вызываем St.bookbron"


("St.bookbron")
async def process_book_name(message: types.Message, state: FSMContext):
    print(f"Запрошеная книга: {message.text}\nОтправте свое местоположение, чтобы мы нашли ближайшую и "
                        f"забронировали нужную вам книгу ", "кнопка отправить свою геолакацию")
   "вызываем  St.bookbron1"
    "создаем переменную со значением того что ввел пользователь"


("вызываеться если мы запршиваем локацию", "St.book")
def process_book_name(message: types.Message, state: FSMContext):
    print("Обрабатываю")
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
                        print(
                            f'В библиотеки по этому адресу есть нужная вам книга: {adress}.\n Название библиотеки: {biblioteka}.\n Вот растояние до этой библиотеки: {shot_rast}.',
                            "кнопка назад")
                    else:
                        print("Название библиотеки не коректное")
            else:
                print("не найдено")
    if b2 == 0:
        print("такой книги нет", "кнопка назад")
    "заканчивает эту фигню "

if __name__ == '__main__':
    worksheet_biblioteki = gsheets()
    worksheet_poisk = knigi()
    executor.start_polling(dp, skip_updates=True)
