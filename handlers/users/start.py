from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.inline.buttons import main_markup
from states.states import AllStates


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    name = message.from_user.username
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
        )
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"@{user[2]} присоединился к базе.\nВ базе {count} пользователя."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    # user = await db.select_user(telegram_id=message.from_user.id)
    await bot.send_message(chat_id=ADMINS[0], text=f"@{name} уже добавлен в базу данных.")
    await message.answer(text="Привет! Я бот, который поможет тебе выбрать группу по твоим интересам", reply_markup=main_markup)
