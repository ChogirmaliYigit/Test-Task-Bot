import pandas as pd
import asyncio
from aiogram import types
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from keyboards.inline.buttons import admin_main_markup

@dp.message_handler(text='/admin', user_id=ADMINS, state="*")
async def login_as_admin(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Выберите опцию.", reply_markup=admin_main_markup)
    await state.finish()

@dp.message_handler(text="/allusers", user_id=ADMINS, state="*")
async def get_all_users(message: types.Message, state: FSMContext):
    await state.finish()
    users = await db.select_all_users()
    if users:
        id = []
        name = []
        for user in users:
            id.append(user[-1])
            name.append(user[1])
        data = {
            "Telegram ID": id,
            "Name": name
        }
        pd.options.display.max_rows = 10000
        df = pd.DataFrame(data)
        if len(df) > 50:
            for x in range(0, len(df), 50):
                await bot.send_message(message.chat.id, df[x:x + 50])
        else:
            await bot.send_message(message.chat.id, df)
    else:
        await message.answer(text="База данных пуста.")
    await state.finish()
       

@dp.callback_query_handler(text="reklama", user_id=ADMINS, state="*")
async def send_ad_to_all(message: types.Message, state: FSMContext):
    await state.finish()
    users = await db.select_all_users()
    for user in users:
        user_id = user[-1]
        await bot.send_message(chat_id=user_id, text="Подписывайтесь на канал @chogirmali_blog!")
        await asyncio.sleep(0.05)
    await state.finish()

@dp.callback_query_handler(text="cleandb", user_id=ADMINS, state="*")
async def get_all_users(message: types.Message, state: FSMContext):
    await state.finish()
    await db.delete_users()
    await message.answer("База очищена!")
    await state.finish()