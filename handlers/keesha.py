from datetime import time

from aiogram.dispatcher import FSMContext
from aiogram import types
from misc import dp, bot
from tools.mitya import St, worksheet_poisk
import keyboards as kb
from misc import worksheet2
import re






@dp.message_handler(text="Нет", state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    print(message.chat.id)
    await message.answer("Вы вернулись на главную страницу", reply_markup=kb.keyboard_menu)
    await state.finish()




@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 1:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                proza = 'проза'
                #print(cv)
                #print(zanr, "1111111")
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('проза')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)

                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    elif code == 2:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('фентези')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)
                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    elif code == 3:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('роман')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)
                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    elif code == 4:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('эротика')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)
                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    elif code == 5:
        for sd in worksheet_poisk:
            print(worksheet_poisk)
            nazvsnie_biblioteki = sd
            spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
            for nekniga in spisok_knig:
                zanr = nekniga["жанр"]
                cv = nekniga['книга']
                zanrr = re.split(',', zanr)
                print(zanrr, 2222)
                zanr_proza = str('детектив')
                print(zanr_proza, 000000)
                for i in zanrr:
                    print(i)
                    if i == zanr_proza:
                        print(zanr_proza, 33333)
                        print(cv, ">>>>", zanr_proza)
                        await bot.send_message(callback_query.from_user.id, f"{cv} >>>> {zanr_proza}")
    else:
        await bot.answer_callback_query(callback_query.id)



@dp.message_handler(text="Поиск книги по жанру")
async def process_command_2(message: types.Message):
    await message.reply("выбирите жанр книги", reply_markup=kb.inline_kb_full)







@dp.message_handler(state=St.otz)
async def otz(message: types.Message, state: FSMContext):
    print("-------")
    for sd in worksheet_poisk:
        print(worksheet_poisk)
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for nekniga in spisok_knig:
            print("---------", nekniga)
            cv = nekniga['книга']
            print("-----------------", cv)
            aid = nekniga['айди']
            print(aid)
            user_id = message.chat.id
            bron = nekniga['бронь']
            ne_bron = "не забронировано"
            print(aid, bron)
            if aid == user_id and bron == ne_bron:  # сравниваем и если не пустата то отсылаем юзеру который в табл сообщение о просьбе оставить отзыв
                print(aid)
                await message.answer(f"вы недавно прочитали книгу '{cv}', не хотите ли оставить отзыв?",
                                             reply_markup=kb.keyboard_net_and_otz)
                time.sleep(10)




@dp.message_handler(text="Оставить отзыв")
async def process_help_command(message: types.Message, state: FSMContext):
    await message.answer("введите отзыв")
    await St.texts.set()



@dp.message_handler(state=St.texts)
async def process_help_command(message: types.Message, state: FSMContext):
    print("+++++++++++++++")
    for sd in worksheet_poisk:
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for nekniga in spisok_knig:
            cv = nekniga['книга']
            aid = nekniga['айди']
            user_id = message.chat.id
            textst = message.text
            bron = nekniga['бронь']
            ne_bron = "не забронировано"
            if bron == ne_bron and aid == user_id:
                lost = [cv, textst, user_id]
                worksheet2.append_row(lost)
                await message.answer("отзыв оставлен")
    await state.finish()




@dp.message_handler(text="Посмотреть отзовы")
async def process_help_command(message: types.Message, state: FSMContext):
    await message.answer("Отзывы к какой книге вы хотите посмотреть?")
    await St.pross.set()


@dp.message_handler(text=St.pross)
async def process_help_command(message: types.Message, state: FSMContext):
    for sd in worksheet_poisk:
        print(worksheet_poisk)
        nazvsnie_biblioteki = sd
        spisok_knig = worksheet_poisk[nazvsnie_biblioteki]
        for nekniga in spisok_knig:
            cv = nekniga['книга']
            aid = nekniga['айди']
            textst = message.text.lower()
            await message.reply(textst)
            otz = nekniga['отзыв']
            if aid != '' and cv == textst:
                await message.answer(f"отзыв о книге{cv}:\n {otz}\n его написал пользователь с id{aid}")



@dp.message_handler(text="Оставить отзыв")
async def process_help_command(msg: types.Message, state: FSMContext):
    await msg.answer("Введите отзыв")
    texts = msg.text
    idd = msg.chat.id
    lost = {idd: texts}
    worksheet2.append_row(lost)




@dp.message_handler()
async def otz(message: types.Message, state: FSMContext):
    print("+++++")
    await St.otz.set()
    print("=====")

