import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import time
import gspread


logging.basicConfig(level=logging.INFO)
bot = Bot(token='1703652201:AAGit3dd0CH4ZgYlWYW-OSRQskn5lTtkeRc')
dp = Dispatcher(bot, storage=MemoryStorage())
na_time = time.strftime('%M')
gc = gspread.service_account()
sh = gc.open("holy buble")
worksheet1 = sh.worksheet("nazvanie").get_all_records()
worksheet2 = sh.worksheet("отзывы").get_all_records()
profil = sh.worksheet("профиль").get_all_records()
knigi_polzovately = sh.worksheet("Книги пользователей").get_all_records()