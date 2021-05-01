from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from misc import dp
from bot import worksheet_biblioteki, worksheet_poisk
from tools.mitya import quick_distance


# Состояния
class St(StatesGroup):
    book0 = State()  # Поиск книги
    book = State()  # Поиск книги
    bookbron = State()  # Бронь книги
    bookbron1 = State()  # Бронь книги


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


@dp.message_handler(text="Карта библиотек")
async def karta(message: types.Message):
    inline_btn_1 = InlineKeyboardButton("Проложить маршрут", url="file:///mapgen/ gafas.html")
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    await message.answer(f'Вот карта библиотек.', reply_markup=kb.keyboard_back)
    await message.answer(f'Если вы хотети её увидеть от нажмите на кнопку под этим сообщением.',
                         reply_markup=inline_kb1)


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
    nalich = 'есть в наличии'
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
    if b2 == 0:
        await message.reply("такой книги нет", reply_markup=kb.keyboard_back)
    await state.finish()


@dp.message_handler(content_types=types.ContentTypes.LOCATION,
                    state=St.bookbron1)  # Функция бронирования после отправки локации
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
    nalichie = 'есть в наличии'
    nevnalichie = "нету в наличии"
    a = 0
    nebron = 'не забронировано'
    for nz in worksheet_poisk:
        nazvanie_biblioteki = nz
        spisok_knig = worksheet_poisk[nazvanie_biblioteki]
        for kn in spisok_knig:
            print(kn)
            kniga = kn['книга']
            kniga1 = kniga.lower()
            bron = kn['бронь']
            nalich = kn['наличие']
            dict = {}
            if kniga1 == text1:
                if nalich == nalichie:
                    if bron == nebron:
                        for bibliotek in worksheet_biblioteki:
                            nazvanie = bibliotek["название"]
                            if nazvanie_biblioteki == nazvanie:
                                dict.update([bibliotek["название"], bibliotek['кординаты']])
                                print(worksheet_poisk)
                                print('Книга найдена!')
                                a = 0
                                f = bibliotek["кординаты"].split(", ")
                                rast = quick_distance(message.location.latitude, message.location.longitude,
                                                      float(f[0]),
                                                      float(f[1]))  # Вычисление растояния до библиотеке.
                                if rast < shot_rast:
                                    shot_rast = rast
                                    adress = bibliotek["адрес"]
                                await message.answer(
                                    f'В библиотеки по этому адресу мы нужную вам книгу: {adress}.\n Название '
                                    f'библиотеки: {nazvanie_biblioteki}.\n Вот растояние до этой библиотеки: '
                                    f'{shot_rast}.', reply_markup=kb.keyboard_back)
                    else:
                        await message.answer('Эта книга забронирована. Вы можете обратиться позже для того чтобы '
                                             'забронировать её.', reply_markup=kb.keyboard_back)
                        print("Данная книга забронирована")
                else:
                    a = a + 1
                    print('Данной книги нету в наличии.')
                    if a == 1:
                        await message.reply("Данной книги нету в наличии.", reply_markup=kb.keyboard_back)
    await state.finish()
