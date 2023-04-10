from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_markup = InlineKeyboardMarkup(row_width=1)
main_markup.insert(InlineKeyboardButton(text="Подобрать группу", callback_data="get_group"))
main_markup.insert(InlineKeyboardButton(text="Список групп", callback_data="groups_list"))


back_button = InlineKeyboardButton('⬅️ Назад', callback_data='back')
back_to_main = InlineKeyboardButton('⬅️ Вернуться в главное меню', callback_data='back_to_main')

back_markup = InlineKeyboardMarkup(row_width=1)
back_markup.insert(back_button)
back_markup.insert(back_to_main)


fields_markup = InlineKeyboardMarkup(row_width=1)
fields_markup.insert(InlineKeyboardButton(text="Психология", callback_data='psychology'))
fields_markup.insert(InlineKeyboardButton(text="Криптовалюта", callback_data='crypto'))
fields_markup.insert(InlineKeyboardButton(text="Стартапы", callback_data='startup'))
fields_markup.insert(back_button)


yes_no_markup = InlineKeyboardMarkup(row_width=2)
yes_no_markup.insert(InlineKeyboardButton(text='Да', callback_data='yes'))
yes_no_markup.insert(InlineKeyboardButton(text='Нет', callback_data='no'))