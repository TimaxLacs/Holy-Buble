from aiogram.utils import executor
from tools.mitya import gsheets, knigi
import handlers
from misc import dp

if __name__ == '__main__':
    worksheet_biblioteki = gsheets()
    worksheet_poisk = knigi()
    executor.start_polling(dp, skip_updates=True)