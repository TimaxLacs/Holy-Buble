from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свою локацию 🗺️', request_location=True))


keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = "Ближащая библиотека"
button_2 = "Узнать о своих книгах"
button_3 = "Найти книгу"
button_4 = "Оставить отзыв"
button_5 = "Забронировать книгу"
button_6 = "Профиль"
button_7 = "Карта библиотек"
keyboard_menu.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7)


keyboard_back = ReplyKeyboardMarkup(resize_keyboard=True)
button_back = KeyboardButton(text="Назад")
keyboard_back.add(button_back)