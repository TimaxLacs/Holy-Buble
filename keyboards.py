from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton





keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = "Ближащая библиотека"
button_2 = "Узнать о своих книгах"
button_3 = "Найти книгу"
button_4 = "Оставить отзыв о книге"
button_5 = "Забронировать книгу"
button_6 = "Профиль"
but_otz = "Оставить отзыв"

button_back = "Назад"
keyboard_menu.add(button_1, button_2, button_3, button_4, button_5, button_6)

but_pros = "просмотреть отзовы"
key_pros = ReplyKeyboardMarkup(resize_keyboard=True)


keyboard_back_and_otz = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_back_and_otz.add(but_otz, button_back)
key_otz = ReplyKeyboardMarkup(resize_keyboard=True)
key_otz.add(but_otz)

keyboard_back = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_back.add(button_back)

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свою локацию 🗺️', request_location=True), button_back)

