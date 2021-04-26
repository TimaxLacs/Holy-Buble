from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свою локацию 🗺️', request_location=True))


keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = "Ближащая библиотека"
button_2 = "Узнать о своих книгах"
button_3 = "Найти книгу"
button_4 = "Оставить отзыв о книге"
button_5 = "Забронировать книгу"
button_6 = "Профиль"
but_otz = "введите отзыв"
but_otz1 = "отправить"
but_otz2 = "оставить отзывы"
button_back = "Назад"
keyboard_menu.add(button_1, button_2, button_3, button_4, button_5, button_6)

but_pros = "просмотреть отзовы"
key_pros = ReplyKeyboardMarkup(resize_keyboard=True)
key_pros.add(but_otz1)

keyboard_back_and_otz = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_back_and_otz.add(but_otz, button_back)
key_otz = ReplyKeyboardMarkup(resize_keyboard=True)
key_otz.add(but_otz)
key_otz1 = ReplyKeyboardMarkup(resize_keyboard=True)
key_otz1.add(but_otz1)
key_otz2 = ReplyKeyboardMarkup(resize_keyboard=True)
key_otz2.add(but_otz2)

keyboard_back = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_back.add(button_back)



