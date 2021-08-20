from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS
from keyboards.inline.menu_keyboards import menu_keyboards
from loader import dp
from utils.db_api.db_commands import get_id_users


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = '<u>Тестовая версия</u>\n' \
          f'Здравствуйте, {message.from_user.full_name}!\n' \
          'Я - Sushi-бот.\n' \
          'Я помогу вам сделать заказ.\n'
    markup = await menu_keyboards()

    if message.from_user.id == int(ADMINS[0]):
        markup.insert(
            KeyboardButton(
                text='⚙ Настройки товара'
            )
        )
        markup.insert(
            KeyboardButton(
                text='✉ Сделать рассылку'
            )
        )
        users = await get_id_users()
        count_users = []
        for user in users:
            count_users.append(user.buyer)
        text += f'\nВсего уникальных пользователей: <b>{len(count_users)}</b> '

    await message.answer(text=text, reply_markup=markup)
    await message.answer_sticker(
                           sticker='CAACAgIAAxkBAAELHeRhB-T-WV-jO2fJNzdVdowWd17K5gACbgUAAj-VzAqGOtldiLy3NSAE')


