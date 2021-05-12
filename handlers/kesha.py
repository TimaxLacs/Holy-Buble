from aiogram.dispatcher import FSMContext
from aiogram import types
from misc import dp
from tools.mitya import St, worksheet_poisk
import keyboards as kb
from misc import worksheet2


@dp.message_handler(text="отз")
async def otz(message: types.Message, state: FSMContext):
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
                                     reply_markup=kb.key_otz)


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
    id = msg.chat.id
    lost = {id: texts}

    worksheet2.append_row(lost)
