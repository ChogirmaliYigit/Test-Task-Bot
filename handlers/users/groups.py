import pandas as pd
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.inline.buttons import main_markup, back_markup, fields_markup, yes_no_markup
from states.states import AllStates
from utils.extra_data import list_of_groups, list_of_links


@dp.callback_query_handler(text='get_group', state='*')
async def get_group(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text='Чем вы интересуетесь?', reply_markup=fields_markup)
    await AllStates.fields.set()

@dp.callback_query_handler(text='back', state=AllStates.fields)
async def back_to_main_from_fields(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Привет! Я бот, который поможет тебе выбрать группу по твоим интересам", reply_markup=main_markup)
    await state.finish()

@dp.callback_query_handler(text='back', state=AllStates.groups_list)
async def go_to_main(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Привет! Я бот, который поможет тебе выбрать группу по твоим интересам", reply_markup=main_markup)
    await state.finish()

@dp.callback_query_handler(text='back_to_main', state='*')
async def go_to_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="Привет! Я бот, который поможет тебе выбрать группу по твоим интересам", reply_markup=main_markup)

@dp.callback_query_handler(text='back', state=AllStates.send_link)
async def back_to_main_from_fields(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='Чем вы интересуетесь?', reply_markup=fields_markup)
    await AllStates.fields.set()

@dp.callback_query_handler(text='back', state=AllStates.link)
async def back_to_main_from_fields(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    field = data.get('field')
    if field == "psychology":
        await call.message.edit_text(text='Вы психолог?', reply_markup=yes_no_markup)
        await AllStates.send_link.set()
    elif field == "crypto":
        await call.message.edit_text(text='Вы торгуете криптовалютой?', reply_markup=yes_no_markup)
        await AllStates.send_link.set()
    elif field == "startup":
        await call.message.edit_text(text='Вы создаете стартап?', reply_markup=yes_no_markup)
        await AllStates.send_link.set()
    await AllStates.send_link.set()

@dp.callback_query_handler(text="psychology", state=AllStates.fields)
async def psychology_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({"field": "psychology"})
    await call.message.edit_text(text='Вы психолог?', reply_markup=yes_no_markup)
    await AllStates.send_link.set()

@dp.callback_query_handler(text="crypto", state=AllStates.fields)
async def psychology_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({"field": "crypto"})
    await call.message.edit_text(text='Вы торгуете криптовалютой?', reply_markup=yes_no_markup)
    await AllStates.send_link.set()

@dp.callback_query_handler(text="startup", state=AllStates.fields)
async def psychology_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({"field": "startup"})
    await call.message.edit_text(text='Вы создаете стартап?', reply_markup=yes_no_markup)
    await AllStates.send_link.set()

@dp.callback_query_handler(state=AllStates.send_link)
async def send_link_to_user(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    field = data.get('field')
    if field == "psychology":
        links = []
        for link in list_of_links.items():
            if link[1] == 'psychology':
                links.append(link[0])
        if links == []:
            call.message.edit_text(text="К сожалению, группы по психологии не найдены.", reply_markup=back_markup)
        elif len(links) == 1:
            await call.message.edit_text(text=f'Была обнаружена одна группа, связанная с психологией: {links[0]}', reply_markup=back_markup)
        else:
            msg = "Ссылки на группы по психологии:\n\n"
            for link in links:
                msg += f'{link}\n'
            await call.message.edit_text(text=msg, reply_markup=back_markup)

    elif field == "crypto":
        links = []
        for link in list_of_links.items():
            if link[1] == 'crypto':
                links.append(link[0])
        if links == []:
            call.message.edit_text(text="К сожалению, криптовалютные группы не найдены.", reply_markup=back_markup)
        elif len(links) == 1:
            await call.message.edit_text(text=f'Найдена одна криптовалютная группа: {links[0]}', reply_markup=back_markup)
        else:
            msg = "Список групп криптовалют:\n\n"
            for link in links:
                msg += f'{link}\n'
            await call.message.edit_text(text=msg, reply_markup=back_markup)

    elif field == "startup":
        links = []
        for link in list_of_links.items():
            if link[1] == 'startup':
                links.append(link[0])
        if links == []:
            call.message.edit_text(text="К сожалению, стартовые группы не найдены.", reply_markup=back_markup)
        elif len(links) == 1:
            await call.message.edit_text(text=f'Нашел одну группу по стартапам: {links[0]}', reply_markup=back_markup)
        else:
            msg = "Список групп по стартапам:\n\n"
            for link in links:
                msg += f'{link}\n'
            await call.message.edit_text(text=msg, reply_markup=back_markup)
    await AllStates.link.set()

@dp.callback_query_handler(text='groups_list', state='*')
async def get_groups_list(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    # Здесь также можно создать список групп через базу данных.
    name = []
    for group in list_of_groups.items():
        name.append(group[1])
    data = {
        "Все группы:": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(call.message.chat.id, df[x:x + 50])
    else:
        await call.message.edit_text(text=df, reply_markup=back_markup)
    await AllStates.groups_list.set()

