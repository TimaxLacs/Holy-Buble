from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = "Ближащая библиотека"
button_2 = "Узнать о своих книгах"
button_3 = "Найти книгу"
button_4 = "Оставить отзыв о книге"
button_5 = "Профиль"
button_6 = "Карта библиотек"
button_7 = "Поиск книг по жанрам"
button_back = "Назад"
button_net = "Нет"
but_pros = "просмотреть отзовы"
button_bron = "Забронировать книгу"
keyboard_menu.add(button_1, button_2).add(button_3, button_4).add(button_5, button_7).add(button_6)


keyboard_net_and_otz = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_net_and_otz.add(button_4, button_net)

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True), button_back)




keyboard_bron = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_bron.add(button_bron, button_back)


key_pros = ReplyKeyboardMarkup(resize_keyboard=True)

inline_btn_1 = InlineKeyboardButton('Проза', callback_data='btn1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_full.add(InlineKeyboardButton('Фентези', callback_data='btn2'))
inline_btn_3 = InlineKeyboardButton('Роман', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('Эротика', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('Детектив', callback_data='btn5')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)



keyboard_back_and_otz = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_back_and_otz.add(button_4, button_back)
key_otz = ReplyKeyboardMarkup(resize_keyboard=True)
key_otz.add(button_4)

keyboard_back = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_back.add(button_back)

button_net = "Нет"

keyboard_net_and_otz = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_net_and_otz.add(button_4, button_net)

