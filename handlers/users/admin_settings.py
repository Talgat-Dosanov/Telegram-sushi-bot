from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentTypes, ReplyKeyboardMarkup, KeyboardButton


from data.config import ADMINS
from keyboards.inline.admin_keyboard import cancel_button, confirm_price, confirm_weight, change_item, transliterator, \
    choose_message_type, photo_markup, text_markup, item_change_menu, confirm_price_changes, confirm_weight_changes, \
    confirm_description_changes, confirm_photo_changes, cancel_delete
from keyboards.inline.menu_keyboards import menu_keyboards
from loader import dp, bot

# Ловим команду создать новый товар
from states import states
from utils.db_api import models
from utils.db_api.db_commands import delete_item, delete_photo, get_id_users, get_subcategory_name, find_item
from utils.db_api.models import Item, Photo


@dp.message_handler(user_id=ADMINS[0], text_contains='⚙ Настройки товара')
async def admin_menu(message: types.Message):
    keyboard = await change_item()
    await message.answer('Меню редактирования товара',
                         reply_markup=keyboard)

@dp.message_handler(user_id=ADMINS[0], text_contains='➕ Создать новый товар')
async def create_item(message: types.Message):
    cancel_btn = await cancel_button()
    await message.answer('Введите название категории', reply_markup=cancel_btn)

    await states.AdminPanel.Category.set()

@dp.message_handler(user_id=ADMINS[0], text_contains='↩ Вернуться')
async def back(message: types.Message):
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
    await message.answer('Меню: ',reply_markup=markup)

# Хендлер отмены
@dp.callback_query_handler(text_contains='cancel', state=states.AdminPanel)
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer('Вы отменили создание товара')
    await state.reset_state()

# Записываем полученную категорию от админа
@dp.message_handler(user_id=ADMINS[0], state=states.AdminPanel.Category)
async def enter_category(message: types.Message, state: FSMContext):
    # Получаем категорию товара из сообщения
    try:
        category_name = str(message.text)
    except ValueError:
        await message.answer('Категория введена неправильно. Введите текст')
        return

    item = models.Item()
    cancel_btn = await cancel_button()
    if category_name.upper() == 'Пицца'.upper():
        item.category_code = 'Pizza'
        item.category_name = '🍕 Пицца'
    elif category_name.upper() == 'Шаурма'.upper():
        item.category_code = 'Shaurma'
        item.category_name = '🌯 Шаурма'
    elif category_name.upper() == 'Wok-Лапша'.upper():
        item.category_code = 'wok-noodles'
        item.category_name = '🥡 Wok-Лапша'
    elif category_name.upper() == 'Бургеры'.upper():
        item.category_code = 'burgers'
        item.category_name = '🍔 Бургеры'
    elif category_name.upper() == 'Закуски'.upper():
        item.category_code = 'snacks'
        item.category_name = '🍟 Закуски'
    if category_name.upper() == 'Суши'.upper():
        item.category_code = 'Sushi'
        item.category_name = '🍣 Суши'
        await message.answer(f'Название категории: {item.category_name}\n\n'
                             'Введите название подкатегории: ',
                             reply_markup=cancel_btn)
        await states.AdminPanel.Subcategory.set()
        await state.update_data(item=item)
    else:
        category_code = await transliterator(category_name)
        item.category_code = category_code
        item.category_name = category_name
        await message.answer(f'Название категории: {item.category_name}\n\n'
                             'Введите название товара: ',
                             reply_markup=cancel_btn)
        item.subcategory_code = '-'
        item.subcategory_name = '-'
        await states.AdminPanel.Name.set()
        await state.update_data(item=item)


# Запрашиваем подкатегорю товара
@dp.message_handler(user_id=ADMINS[0], state=states.AdminPanel.Subcategory)
async def enter_subcategory(message: types.Message, state: FSMContext):
    # Записываем полученную подкатегорию товара
    try:
        subcategory = str(message.text)
    except ValueError:
        await message.answer('Подкатегория введена неправильно. Введите текст')
        return

    data = await state.get_data()
    item: models.Item = data.get('item')
    item.subcategory_name = subcategory
    if item.category_name == '🍣 Суши':
        subcategory_code = await get_subcategory_name(str(subcategory))
        text = subcategory_code.subcategory_code
    else:
        text = await transliterator(subcategory)
    print(text)
    item.subcategory_code = text

    # Кнопка отмены
    cancel_btn = await cancel_button()

    await message.answer(f'Название категории: {item.category_name}\n\n'
                         f'Название подкатегории: {item.subcategory_name}\n'
                         'Введите название товара: ',
                          reply_markup=cancel_btn)
    await states.AdminPanel.Name.set()
    await state.update_data(item=item)

# Ловим имя товара
@dp.message_handler(user_id=ADMINS[0], state=states.AdminPanel.Name)
async def enter_name(message: types.Message, state: FSMContext):
    # Получаем имя товара
    name = message.text
    cancel_btn = await cancel_button()
    # Вытаскиваем значение item из state
    data = await state.get_data()
    item: models.Item = data.get('item')
    item.name = name

    await message.answer(f'Название категории: {item.category_name}\n'
                         f'Название товара: {name}\n\n'
                         'Пришлите фото товара (прикрепив фото к пустому сообщению)',
                            reply_markup=cancel_btn)

    await states.AdminPanel.Photo.set()
    await state.update_data(item=item)

# Ловим фото товара
@dp.message_handler(user_id=ADMINS[0], state=states.AdminPanel.Photo, content_types=ContentTypes.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):

    # Получаем фото товара и сохраняем в state
    photo = message.photo[-1].file_id
    cancel_btn = await cancel_button()
    data = await state.get_data()
    item: models.Item = data.get('item')

    await message.answer_photo(photo=photo,
                               caption=(f'Название категории товара: {item.category_name}\n'
                                        f'Название товара: {item.name}\n\n'
                                        'Введите описание товара описание товара'),
                               reply_markup=cancel_btn)
    await states.AdminPanel.Description.set()
    await state.update_data(photo=models.Photo(
        file_id=photo,
        filename=item.name,
        product=item.name
    )
    )
# Создаем описание товара
@dp.message_handler(user_id=ADMINS[0], state=states.AdminPanel.Description)
async def enter_description(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    item: models.Item = data.get('item')
    item.description = description
    cancel_btn = await cancel_button()

    await message.answer(f'Название категории товара: {item.category_name}\n'
                         f'Название товара: {item.name}\n\n'
                         'Введите цену товара в рублях',reply_markup=cancel_btn)

    await states.AdminPanel.Price.set()
    await state.update_data(item=item)

# Создаем цену товара
@dp.message_handler(user_id=ADMINS[0], state=states.AdminPanel.Price)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item: models.Item = data.get('item')
    try:
        price = int(message.text)
    except ValueError:
        await message.answer('Неверное значение. Пожалуйста введите число')
        return

    item.price = price
    markup = await confirm_price()
    text = f'Название категории товара: {item.category_name}\n'\
           f'Название товара: {item.name}\n'\
           f'Цена товара: {item.price} руб.\n\n' \



    await state.update_data(item=item)
    await message.answer(text=text, reply_markup=markup)

    await states.AdminPanel.Weight.set()

@dp.callback_query_handler(user_id=ADMINS[0],text_contains='price_change',state=states.AdminPanel.Weight)
async def change_price(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.edit_text('Введите заново цену товара в рублях')

    await states.AdminPanel.Price.set()

# Запрашиваем массу товара
@dp.callback_query_handler(user_id=ADMINS[0],text_contains='price_confirm', state=states.AdminPanel.Weight)
async def enter_weight(call: CallbackQuery):
    await call.message.edit_text('Введите вес товара в граммах')
    await states.AdminPanel.Weight.set()

# Записываем массу товара
@dp.message_handler(user_id=ADMINS[0], state=states.AdminPanel.Weight)
async def enter_weight(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item: models.Item = data.get('item')

    weight_keyboard = await confirm_weight()
    photo: models.Photo = data.get('photo')
    try:
        weight = int(message.text)
    except ValueError:
        await message.answer('Неверное значение веса. Введите число')
        return

    item.weight = weight
    if item.subcategory_name != '-':
        await message.answer_photo(photo=photo.file_id,caption=
                             f'Название категории товара: {item.category_name}\n'
                             f'Название подкатегории товара:{item.subcategory_name}\n'
                             f'Название товара: {item.name}\n'
                             f'Цена товара: {item.price} руб.\n'
                             f'Масса товара {weight} гр.',
                             reply_markup=weight_keyboard)
    else:
        await message.answer_photo(photo=photo.file_id, caption=
                            f'Название категории товара: {item.category_name}\n'
                            f'Название товара: {item.name}\n'
                            f'Цена товара: {item.price} руб.\n'
                            f'Масса товара {weight} гр.',
                            reply_markup=weight_keyboard)

    await state.update_data(item=item)
    await states.AdminPanel.Confirm.set()

# Изменяем массу товара
@dp.callback_query_handler(user_id=ADMINS[0],text_contains='weight_change',state=states.AdminPanel.Confirm)
async def change_price(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer('Введите заново вес товара в граммах')

    await states.AdminPanel.Weight.set()

# Подтверждаем создание товара
@dp.callback_query_handler(user_id=ADMINS[0], text_contains='confirm_weigth', state=states.AdminPanel.Confirm)
async def confirm(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item: models.Item = data.get('item')
    photo: models.Photo = data.get('photo')

    await item.create()
    await photo.create()
    await call.message.answer('Товар успешно создан!')
    await state.reset_state()

# Функция удаления товара из базы
@dp.message_handler(user_id=ADMINS[0], text_contains='❌ Удалить товар',)
async def enter_item_name(message: types.Message):
    markup = await cancel_delete()
    await message.answer('Введите название товара который хотите удалить',reply_markup=markup)
    await states.DeleteItem.Item.set()

@dp.callback_query_handler(user_id=ADMINS[0], text_contains='cancel_delete',state=states.DeleteItem.Item)
async def cancel_del(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.message.edit_text('Функция удаления отменена!')


# Ловим имя товара и удаляем его
@dp.message_handler(user_id=ADMINS[0], state=states.DeleteItem.Item)
async def del_item(message: types.Message, state: FSMContext):
    item = message.text
    await delete_item(item)
    await delete_photo(item)
    await state.reset_state()
    await message.answer('Товар успешно удален!')

# Функция рассылки
@dp.message_handler(user_id=ADMINS[0], text_contains='✉ Сделать рассылку')
async def message(message: types.Message):
    markup = await choose_message_type()
    await message.answer('Выберите тип рассылки',
                         reply_markup=markup)

# Функция отмены рассылки
@dp.callback_query_handler(user_id=ADMINS[0], text_contains="back_to_the_menu")
async def kill_mailing(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Вы отменили рассылку')


# Функция отмены рассылки
@dp.callback_query_handler(user_id=ADMINS[0], text_contains="cancel_mailing", state=states.Mailing)
async def kill_mailing(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='Вы отменили рассылку')
    await state.reset_state()

@dp.callback_query_handler(user_id=ADMINS[0], text_contains='text_mailing')
async def enter_mailing_text(call: CallbackQuery):
    # Запрашиваем текст сообщения
    await call.message.edit_text('Введите текст сообщения')
    await states.Mailing.Text.set()


@dp.callback_query_handler(user_id=ADMINS[0], text_contains='photo_mailing')
async def send_photo_mailing(call: CallbackQuery):
    await call.message.edit_text('Прикрепите фото к сообщению ')

    await states.Mailing.Photo.set()

@dp.message_handler(user_id=ADMINS[0], state=states.Mailing.Text, content_types=ContentTypes.TEXT)
async def mailtext(message: types.Message, state: FSMContext):
    markup = await text_markup()
    await message.answer(text='Введите текст рассылки',
                            reply_markup=markup)
    await states.Mailing.Confirm.set()


@dp.message_handler(user_id=ADMINS[0], state=states.Mailing.Photo, content_types=ContentTypes.PHOTO)
async def photo_mailing(message: types.Message, state: FSMContext):
    text = message.caption
    markup = await photo_markup()
    photo = message.photo[-1].file_id
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)
    await state.update_data(photo=photo, caption=text)
    await states.Mailing.Confirm.set()

@dp.callback_query_handler(user_id=ADMINS[0], text_contains='accept_photo',state=states.Mailing.Confirm)
async def confirm_photo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photo = data.get('photo')
    caption = data.get('caption')
    users = await get_id_users()

    for user in users:
        try:
            await bot.send_photo(chat_id=user.buyer, photo=photo, caption=caption)

            await sleep(0.3)
        except Exception:
            pass
    await state.reset_state()
    await call.message.answer('Рассылка выполнена!')

@dp.callback_query_handler(user_id=ADMINS[0], text_contains='accept_text', state=states.Mailing.Confirm)
async def confirm_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    users = await get_id_users()

    for user in users:
        try:
            await bot.send_text(chat_id=user.buyer, text=text)

            await sleep(0.3)
        except Exception:
            pass
    await state.reset_state()
    await message.answer('Рассылка выполнена!')

# Функция изменения товара
@dp.message_handler(user_id=ADMINS[0], text_contains='🔧 Изменить товар')
async def change_items(message: types.Message):
    await message.answer('Введите название товара')
    await states.ChangeItem.ItemName.set()

# Ловим название товара и предлагаем варианты изменения
@dp.message_handler(user_id=ADMINS[0], state=states.ChangeItem.ItemName)
async def item_name(message: types.Message, state: FSMContext):
    # сохраняем название товара в state
    itemName = message.text

    try:
        item = await Item.query.where(Item.name == itemName).gino.first()
        await state.update_data(item_name=item.name)
    except Exception:
        await message.answer('Такого товара не существует. Пожалуйста введите название товара еще раз')
        return



    markup = await item_change_menu()

    await message.answer(text=f'<u>Категория товара</u>: <code> {item.category_name}</code>\n'
                                 f'<u>Подкатегория товара:</u> <code> {item.subcategory_name}</code>\n'
                                 f'<u>Название товара:</u> <code> {item.name}</code>',
                        reply_markup=markup)

    await states.ChangeItem.ItemName.set()



# Функция изменения цены
@dp.callback_query_handler(user_id=ADMINS[0], text_contains='item_change_price', state=states.ChangeItem.ItemName)
async def process_change_price(call: CallbackQuery):
    await call.message.edit_text(text='Введите новую цену товара')
    await states.ChangeItem.Price.set()

# Функция изменения веса
@dp.callback_query_handler(user_id=ADMINS[0], text_contains="item_change_weight", state=states.ChangeItem.ItemName)
async def process_change_weight(call: CallbackQuery):
    await call.message.edit_text(text='Введите новую массу товара')
    await states.ChangeItem.Weight.set()

# Функция изменения описания
@dp.callback_query_handler(user_id=ADMINS[0], text_contains="item_change_description", state=states.ChangeItem.ItemName)
async def process_change_desc(call: CallbackQuery):
    await call.message.edit_text(text='Введите новое описание товара')
    await states.ChangeItem.Description.set()


# Функция изменения фото
@dp.callback_query_handler(user_id=ADMINS[0], text_contains="change_photo_command", state=states.ChangeItem.ItemName)
async def process_change_desc(call: CallbackQuery):
    await call.message.answer(text='Прикрепите фото к пустому сообщению и нажмите <i>Отправить</i>')
    await states.ChangeItem.Photo.set()

# Отмена
@dp.callback_query_handler(user_id=ADMINS[0], text_contains="cancel_command", state=states.ChangeItem)
async def process_change_desc(call: CallbackQuery,state: FSMContext):
    await call.message.answer(text='Вы отменили изменение товара')
    await state.reset_state()

# Сохраняем цену в state
@dp.message_handler(user_id=ADMINS[0], state=states.ChangeItem.Price)
async def change_price_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item_name = data.get('item_name')
    item = await Item.query.where(Item.name == item_name).gino.first()
    photo = await Photo.query.where(Photo.product == item_name).gino.first()
    try:
        price = int(message.text)
    except ValueError:
        await message.answer('Ошибка ввода цены. Введите число')
        return

    markup = await confirm_price_changes()
    await message.answer_photo(photo=photo.file_id,
                               caption=f'<b>Категория товара</b>: <code> {item.category_name}</code>\n'
                                 f'<b>Подкатегория товара:</b> <code> {item.subcategory_name}</code>\n'
                                 f'<b>Название товара:</b> <code> {item.name}</code>\n'
                                 f'<b>Цена товара:</b> <code> {price}</code>',
                               reply_markup=markup)

    await state.update_data(price=price)
    await states.ChangeItem.ConfirmChanges.set()


# Сохраняем вес в state
@dp.message_handler(user_id=ADMINS[0], state=states.ChangeItem.Weight)
async def change_price_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item_name = data.get('item_name')
    item = await Item.query.where(Item.name == item_name).gino.first()
    photo = await Photo.query.where(Photo.product == item_name).gino.first()
    try:
        weight = int(message.text)
    except ValueError:
        await message.answer('Ошибка ввода веса. Введите число')
        return

    markup = await confirm_weight_changes()
    await message.answer_photo(photo=photo.file_id,
                               caption=f'<b>Категория товара</b>: <code> {item.category_name}</code>\n'
                                 f'<b>Подкатегория товара:</b> <code> {item.subcategory_name}</code>\n'
                                 f'<b>Название товара:</b> <code> {item.name}</code>\n'
                                 f'<b>Цена товара:</b> <code> {item.price}</code>\n'
                                 f'<b>Вес товара:</b> <code> {weight}</code>'
                                 ,
                               reply_markup=markup)

    await state.update_data(weight=weight)
    await states.ChangeItem.ConfirmChanges.set()


# Сохраняем описание в state
@dp.message_handler(user_id=ADMINS[0], state=states.ChangeItem.Description)
async def change_price_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item_name = data.get('item_name')
    item = await Item.query.where(Item.name == item_name).gino.first()
    photo = await Photo.query.where(Photo.product == item_name).gino.first()
    description = message.text


    markup = await confirm_description_changes()
    await message.answer_photo(photo=photo.file_id,
                               caption=f'<b>Категория товара</b>: <code> {item.category_name}</code>\n'
                                       f'<b>Подкатегория товара:</b> <code> {item.subcategory_name}</code>\n'
                                       f'<b>Название товара:</b> <code> {item.name}</code>\n'
                                       f'<b>Цена товара:</b> <code> {item.price}</code>\n'
                                       f'<b>Вес товара:</b> <code> {item.weight}</code>\n'
                                       f'<b>Состав:\n</b> <code> {description}</code>'
                               ,
                               reply_markup=markup)

    await state.update_data(description=description)
    await states.ChangeItem.ConfirmChanges.set()


# Сохраняем фото в state
@dp.message_handler(user_id=ADMINS[0], state=states.ChangeItem.Photo,content_types=ContentTypes.PHOTO)
async def change_price_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item_name = data.get('item_name')
    item = await Item.query.where(Item.name == item_name).gino.first()
    photo = message.photo[-1].file_id

    markup = await confirm_photo_changes()
    await message.answer_photo(photo=photo,
                               caption=f'<b>Категория товара</b>: <code> {item.category_name}</code>\n'
                                       f'<b>Подкатегория товара:</b> <code> {item.subcategory_name}</code>\n'
                                       f'<b>Название товара:</b> <code> {item.name}</code>\n'
                                       f'<b>Цена товара:</b> <code> {item.price}</code>\n'
                                       f'<b>Вес товара:</b> <code> {item.weight}</code>'
                               ,
                               reply_markup=markup)

    await state.update_data(photo=photo)
    await states.ChangeItem.ConfirmChanges.set()

# Записываем изменения цены в базу данных
@dp.callback_query_handler(user_id=ADMINS[0],text_contains='ConfirmChangesPrice', state=states.ChangeItem.ConfirmChanges)
async def confirm_price_change(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_name = data.get('item_name')
    price = data.get('price')

    await state.reset_state()
    await call.message.answer('Товар изменен!')

    await Item.update.values(price=price).where(Item.name == item_name).gino.scalar()

# Записываем изменения цены в базу данных
@dp.callback_query_handler(user_id=ADMINS[0],text_contains='ConfirmWeightChanges', state=states.ChangeItem.ConfirmChanges)
async def confirm_weigh_change(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_name = data.get('item_name')
    weight = data.get('weight')

    await state.reset_state()
    await call.message.answer('Товар изменен!')

    await Item.update.values(weight=weight).where(Item.name == item_name).gino.scalar()

@dp.callback_query_handler(user_id=ADMINS[0],text_contains='ConfirmDescChanges', state=states.ChangeItem.ConfirmChanges)
async def confirm_desc_change(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_name = data.get('item_name')
    description = data.get('description')

    await state.reset_state()
    await call.message.answer('Товар изменен!')

    await Item.update.values(description=description).where(Item.name == item_name).gino.status()

@dp.callback_query_handler(user_id=ADMINS[0],text_contains='ConfirmPhotoChanges', state=states.ChangeItem.ConfirmChanges)
async def confirm_photo_change(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_name = data.get('item_name')
    photo = data.get('photo')

    await state.reset_state()
    await call.message.answer('Товар изменен!')

    await Photo.update.values(file_id=photo).where(Photo.product == item_name).gino.status()
