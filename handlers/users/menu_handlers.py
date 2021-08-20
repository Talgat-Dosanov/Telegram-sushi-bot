import json
from typing import Union
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, LabeledPrice, ContentTypes, InlineKeyboardMarkup, \
    InlineKeyboardButton, InputMediaPhoto, InputMedia, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from data.config import LP_TOKEN, ADMINS
from keyboards.inline.menu_keyboards import menu_cd, categories_keyboard, \
    items_keyboard, item_keyboard, buy_item, make_callback_data, menu_keyboards, input_keyboard, delivery_keyboard, \
    shipping_keyboard, subcategories_keyboard, phoneNumber_markup
from loader import dp, bot
from states import states
from utils.db_api.db_commands import get_item, get_categories, get_photo, get_items_from_shipping_cart, delete_cart, \
    get_order
from utils.db_api import models
from keyboards.inline.admin_keyboard import support_callback, order_for_admins, ready_keyboard, ready_button_callback


# Хендлер на команду /menu
from utils.db_api.models import PurchaseItem


@dp.message_handler(text_contains='🍴 Меню')
async def show_menu(message: types.Message):
    # Выполним функцию, которая отправит пользователю кнопки с доступными категориями
    await list_categories(message)

# Корзина
@dp.message_handler(text_contains='🛒 Корзина')
async def show_cart(message: types.Message, state: FSMContext):


    clean_cart = InlineKeyboardButton(
        text='Очистить корзину',
        callback_data='clean'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [clean_cart]
        ]
    )

    user_id = int(message.from_user.id)
    cart = await get_items_from_shipping_cart(user_id)
    items_from_cart = []


    for item in cart:
        items_from_cart.append((str(item.item_name) + ' - ' + str(int(item.amount) / int(item.quantity)) + ' руб/шт ' + ' - ' + str(item.quantity) +'/шт'))
    items_from_cart = '\n🔹 '.join(items_from_cart)

    await message.answer(text='Ваш заказ 🛎:\n'+'🔹 ' + items_from_cart, reply_markup=markup)

@dp.callback_query_handler(text_contains='clean')
async def clean_cart(call:CallbackQuery):
    user_id = call.from_user.id
    await delete_cart(user_id)
    await call.message.edit_text(text='Корзина очищена!')



# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await categories_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("Смотри, что у нас есть", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


# Функция, которая отдает кнопки с подкатегориями, по выбранной пользователем категории
async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_reply_markup(markup)


# Функция, которая отдает кнопки с Названием и ценой товара, по выбранной категории и подкатегории
async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category, subcategory)

    # Изменяем клавиатуру, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_reply_markup(reply_markup=markup)


# Функция, которая отдает кнопку Купить товар по выбранному товару
async def show_item(callback: CallbackQuery, category, item_id, subcategory):
    markup = item_keyboard(category=category, subcategory=subcategory, item_id=item_id)

    item = await get_item(item_id)
    photo = await get_photo(item.name)

    # Берем запись о нашем товаре из базы данных
    text = "<b>{category_name}:</b> {item_name}\n" \
           "<b>Цена:</b> {price} <b>руб.</b>\n" \
           "<b>Вес:</b> {weight} <b>г.</b>\n" \
           "<b>Состав:</b>\n" \
           "<code>{description}</code>\n".format(category_name=item.category_name,
                                    item_name=item.name,
                                     price=item.price,
                                     weight=item.weight,
                                     description=item.description)
    await callback.message.answer_photo(photo=photo.file_id,
                                        caption=text,
                                        reply_markup=markup)


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    category = callback_data.get("category")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    subcategory = callback_data.get("subcategory")

    # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    item_id = int(callback_data.get("item_id"))

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    if category == 'Sushi':
        levels = {
            "0": list_categories,  # Отдаем категории
            "1": list_subcategories, # Отдаем подкатегории
            "2": list_items,  # Отдаем товары
            "3": show_item  # Предлагаем купить товар
        }
    else:
        levels = {
            "0": list_categories,  # Отдаем категории
            "1": list_items,  # Отдаем товары
            "2": show_item  # Предлагаем купить товар
        }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    if category == 'Sushi':
        await current_level_function(
            call,
            category=category,
            subcategory=subcategory,
            item_id=item_id
        )
    else:
        await current_level_function(
            call,
            category=category,
            item_id=item_id,
            subcategory=subcategory
        )

# Выводим клавиатуру для ввода количества товара
@dp.callback_query_handler(buy_item.filter())
async def purchase_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    # Создаем кнопки ввода
    button1 = KeyboardButton('1')
    button2 = KeyboardButton('2')
    button3 = KeyboardButton('3')
    button4 = KeyboardButton('4')
    button5 = KeyboardButton('5')
    button6 = KeyboardButton('6')
    button7 = KeyboardButton('7')
    button8 = KeyboardButton('8')
    button9 = KeyboardButton('9')
    num_keyboard = ReplyKeyboardMarkup(row_width=3).add(
        button1,button2,button3,
        button4,button5,button6,
        button7,button8,button9
    )

    await call.message.edit_reply_markup()
    await call.message.answer('Введите количество товара:', reply_markup=num_keyboard)

    item_id = int(callback_data.get('item_id'))

    item = await get_item(int(item_id))


    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        )
    )

    await states.NewItem.EnterQuality.set()
    await state.update_data(item=item,
                            purchase=models.PurchaseItem(
                            item_name=item.name,
                            buyer=call.from_user.id
                            ),
                            item_id=int(item_id),
                            item_price=item.price
                            )
    await states.NewItem.EnterQuality.set()

# Ловим количество товара
@dp.message_handler(regexp=r'^(\d+)$', state=states.NewItem.EnterQuality)
async def enter_quality(message: types.Message, state: FSMContext):
    await message.answer('Принято ✅',reply_markup=ReplyKeyboardRemove())
    # получаем количество товара
    quantity = int(message.text)
    async with state.proxy() as data: # работа с данными FSM

        data['quantity'] = quantity
        item = data['item']
        amount = item.price * quantity
        data['amount'] = amount


    # Создаем кнопки
    agree_button = InlineKeyboardButton(
        text='Оформить заказ',
        callback_data='order'
    )

    add_to_sc = InlineKeyboardButton(
        text='Добавить в корзину',
        callback_data='add_to_order'
    )


    change_button = InlineKeyboardButton(
        text='Ввести заново',
        callback_data='change_amount'
    )
    cancel_button = InlineKeyboardButton(
        text='Отменить покупку',
        callback_data='cancel'
    )


    #Создаем клавиатуру
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [agree_button], #Первый ряд
            [add_to_sc], #Второй ряд
            [change_button],  # Третий ряд
            [cancel_button]  #Третий ряд
        ]
    )
    await message.answer(text=
        f'Ваш заказ {item.name} {quantity} шт.\n'
        f'На сумму: {amount} руб.',
        reply_markup=markup
    )

    await states.NewItem.Order.set()

# То что, не является числом попадает в этот хендлер
@dp.message_handler(state=states.NewItem.EnterQuality)
async def not_quantity(message: types.Message):
    await message.answer('Неверное значение, введите число')

# При нажатии кнопки отмена попадаем в этот хендлер
@dp.callback_query_handler(text_contains='cancel', state=states.NewItem)
async def process_cancel(call: CallbackQuery, state: FSMContext):
    markup = await menu_keyboards()
    await call.message.edit_text('Вы отменили покупку')
    await call.message.answer('✅ Принято', reply_markup=markup)
    await state.reset_state()

# При изменении значения количества товара попадаем сюда
@dp.callback_query_handler(text_contains='change_amount', state=states.NewItem.Order)
async def change(call: CallbackQuery):
    num_keyboard = await input_keyboard()
    await call.message.answer('⬇', reply_markup=num_keyboard)
    await call.message.edit_text('Введите количество товара заново: ')

    await states.NewItem.EnterQuality.set()

# Хендлер корзины
@dp.callback_query_handler(text_contains='add_to_order', state=states.NewItem.Order)
async def add_to_order(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    shopping_cart = models.ShoppingCart
    item: models.Item = data.get('item')
    purchase: models.PurchaseItem = data.get('purchase')
    item_id = item.price
    item_name = purchase.item_name
    user_id = call.from_user.id
    amount = data.get('amount')
    quantity = int(amount) / int(item.price)

    await shopping_cart.create(
        item_id=item_id,
        item_name=item_name,
        user_id=user_id,
        quantity=quantity,
        amount=amount
    )


    await state.reset_state()

    keyboard = await menu_keyboards()

    await call.message.edit_text(text=f'Вы добавили к заказу {item_name}')
    await call.message.answer('Нажмите <code>🍴 Меню</code>, чтобы перейти к категориям товаров', reply_markup=keyboard)

# Вывод информации по заказу
@dp.callback_query_handler(text_contains='order', state=states.NewItem.Order)
async def order_info_command(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    purchase: models.PurchaseItem = data.get('purchase')


    await models.ShoppingCart.create(
        user_id=call.from_user.id,
        item_id=data.get('item_id'),
        item_name=purchase.item_name,
        quantity=data.get('amount') / data.get('item_price'),
        amount=data.get('amount')
    )
    user_id = purchase.buyer
    shopping_cart = await get_items_from_shipping_cart(user_id)
    item_name = []
    total_amount = 0
    for item in shopping_cart:
        item_name.append((str(item.item_name) + ' - ' + str(item.quantity) + '/шт'))
        total_amount += item.amount

    item_name = '\n'.join(item_name)
    keyboard = await delivery_keyboard()
    await call.message.edit_text(
        text=f'Ваш заказ:\n'
             f'{item_name}\n'
             f'На сумму: {total_amount} руб.',
        reply_markup=keyboard
    )
    await states.NewItem.Approval.set()

# Просим пользователя ввести адрес доставки
@dp.callback_query_handler(text_contains='delivery', state=states.NewItem.Approval)
async def delivery_command(call: CallbackQuery):
    await call.message.edit_text('Введите адрес доставки\n'
                                 '"<i>Например: ул. Советская, д.6, кв. 3"</i>')

    await states.NewItem.Delivery.set()

# Ловим адрес доставки с помощью хендлера
@dp.message_handler(regexp=r'(. \d+)|[/]', state=states.NewItem.Delivery)
async def get_shipping_address(message: types.Message,state: FSMContext):
    shipping_address = message.text

    markup = await shipping_keyboard()
    await message.answer(text='Ваш адрес доставки:\n'
                                 f'{shipping_address}',
                            reply_markup=markup)
    await state.update_data(
        shipping_address=shipping_address,
        delivery_method='Доставка'
    )
    await states.NewItem.Approval.set()

@dp.message_handler(state=states.NewItem.Delivery)
async def wrong_shipping_address(message: types.Message):
    await message.answer('Неправильный адрес доставки! Повторите попытку.')

# Хедлер при изменении адреса доставки
@dp.callback_query_handler(text_contains='change_shipping_address', state=states.NewItem.Approval)
async def change_shipping_address(call: CallbackQuery):
    await call.message.edit_text('Введите адрес доставки заново!')

    await states.NewItem.Delivery.set()



# Спрашиваем номер телефона для связи c пользователем
@dp.callback_query_handler(text_contains='phone_number_pickup',state=states.NewItem.Approval)
async def ask_phone_number_pickup(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    await state.update_data(delivery_method='Самовывоз',
                            user_id=user_id)
    markup = await phoneNumber_markup()
    try:
        user = await PurchaseItem.select('phone_number').where(PurchaseItem.buyer == user_id).gino.scalar()
        if user == None:
            raise AttributeError
        await call.message.edit_text(f'☎ Ваш номер телефона: {user}', reply_markup=markup)
        await states.NewItem.Approval.set()
    except AttributeError:
        await call.message.edit_text(f'☎ Введите номер телефона для связи')
        await states.NewItem.PhoneNumber.set()



# Функция самовывоза
@dp.callback_query_handler(text_contains='pickup', state=states.NewItem.Approval)
async def process_pickup_command(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    print(user_id)

    phone_number = await PurchaseItem.select('phone_number').where(PurchaseItem.buyer == user_id).gino.scalar()
    if phone_number == None:
        phone_number = data.get('phone_number')
    await state.update_data(
        phone_number=phone_number
    )



    data = await state.get_data()
    purchase: models.PurchaseItem = data.get('purchase')

    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(
        text='Подтвердить заказ',
        callback_data='accept'
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text='Отменить заказ',
            callback_data='cancel'
        )
    )
    user_id = purchase.buyer
    shopping_cart = await get_items_from_shipping_cart(user_id)
    item_name = []
    total_amount = 0
    delivery_method = data.get('delivery_method')
    for item in shopping_cart:
        item_name.append((str(item.item_name) + ' - ' + str(item.quantity) + '/шт'))
        total_amount += item.amount

    item_name = '\n'.join(item_name)
    await call.message.edit_text(text=f'Ваш заказ:\n'
             f'{item_name}\n'
             f'Ваш номер телефона: {phone_number}\n'
             f'На сумму: {total_amount} руб\n.'
             f'Способ доставки: {delivery_method}',
        reply_markup=keyboard)


    await states.NewItem.Approval.set()

# Спрашиваем номер телефона для связи c пользователем
@dp.callback_query_handler(text_contains='phone',state=states.NewItem.Approval)
async def ask_phone_number(call: CallbackQuery):
    await call.message.edit_text('☎ Введите номер телефона для связи')


    await states.NewItem.PhoneNumber.set()

# Заносим телефон в state
@dp.message_handler(regexp=r'\b\d{11}\b', state=states.NewItem.PhoneNumber)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = int(message.text)
    markup =InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Принять',
            callback_data='description'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Ввести заново',
            callback_data='change_phone_number'
        )
    )
    await message.answer('Ваш номер для связи:\n'
                            f'{phone_number}',
                            reply_markup=markup
                            )
    await state.update_data(
        phone_number=phone_number
    )
    await states.NewItem.Approval.set()

@dp.message_handler(state=states.NewItem.PhoneNumber)
async def wrong_phone_number(message: types.Message):
    await message.answer('Неверный номер телефона. Пожалуйста повторите попытку.')

@dp.callback_query_handler(text_contains='change_phone_number', state=states.NewItem.Approval)
async def change(call: CallbackQuery):

    await call.message.edit_text('Введите номер телефона заново: ')
    await states.NewItem.PhoneNumber.set()


@dp.callback_query_handler(text_contains='description', state=states.NewItem.Approval)
async def description_order(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    delivery_method = data.get('delivery_method')
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        text='Да',
        callback_data='note'
    )
    )
    if delivery_method == 'Самовывоз':
        markup.row(InlineKeyboardButton(
            text='Нет',
            callback_data='pickup'
        )
        )
    else:
        markup.row(InlineKeyboardButton(
            text='Нет',
            callback_data='accept'
        )
        )
    await call.message.answer('Добавить примечание к заказу?', reply_markup=markup)
    await states.NewItem.Approval.set()

@dp.callback_query_handler(text_contains='note', state=states.NewItem.Approval)
async def enter_description(call: CallbackQuery):
    await call.message.edit_text('Введите текст примечания')

    await states.NewItem.Note.set()

@dp.message_handler(state=states.NewItem.Note)
async def save_note(message: types.Message, state: FSMContext):
    text = message.text
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='ОК',
            callback_data='accept'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Ввести заново',
            callback_data='enter_again'
        )
    )
    await message.answer(text=text, reply_markup=markup)
    await state.update_data(note=text)
    await states.NewItem.Approval.set()

@dp.callback_query_handler(text_contains='enter_again', state=states.NewItem.Approval)
async def enter_description(call: CallbackQuery):
    await call.message.edit_text('Введите текст примечания')
    await states.NewItem.Note.set()

@dp.callback_query_handler(text_contains='accept', state=states.NewItem.Approval)
async def send_admins(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    purchase: models.PurchaseItem = data.get('purchase')
    user_id = purchase.buyer
    shopping_cart = await get_items_from_shipping_cart(user_id)
    item_name = []
    if data.get('delivery_method') == 'Доставка':
        total_amount = 100
    else:
        total_amount = 0
    for item in shopping_cart:
        item_name.append((str(item.item_name) + ' - ' + str(item.quantity) + '/шт'))
        total_amount += item.amount
    item_name = '\n'.join(item_name)
    await purchase.create()
    await purchase.update(
        item_name=item_name,
        receiver=call.from_user.full_name,
        purchase_time=datetime.datetime.now(),
        amount=total_amount,
        shipping_address=data.get('shipping_address'),
        phone_number=str(data.get('phone_number')),
        delivery_method=data.get('delivery_method'),
        note=data.get('note')

    ).apply()
    if purchase.delivery_method == 'Доставка':
        order_info = 'Получен заказ!\n' \
                     f'👤 Имя заказчика: {purchase.receiver}\n' \
                     f'🔑 ID пользователя: {purchase.buyer}\n' \
                     f'☎ Номер телефона: {purchase.phone_number}\n' \
                     f'🚚 Адрес доставки: {purchase.shipping_address}\n' \
                     f'🛎 Заказ:\n' \
                     f'{item_name}\n' \
                     f'💵 Сумма заказа: {purchase.amount} руб\n' \
                     f'💵 Сумма доставки: 100 руб\n' \
                     f'💰 Итоговая сумма: {purchase.amount + 100} руб\n' \
                     f'📜 Примечание к заказу:\n ' \
                     f'{purchase.note}'

    else:
        order_info = f'Получен заказ №{purchase.id}!\n' \
                     f'👤 Имя заказчика: {purchase.receiver}\n' \
                     f'🔑 ID пользователя: {purchase.buyer}\n' \
                     f'☎ Номер телефона: {purchase.phone_number}\n' \
                     f'🚚 Способ доставки: {purchase.delivery_method}\n' \
                     f'🛎 Заказ:\n' \
                     f'{purchase.item_name}\n' \
                     f'💰 Сумма заказа: {purchase.amount} руб\n' \
                     f'📜 Примечание к заказу:\n ' \
                     f'{purchase.note}'



    keyboard_for_admins = order_for_admins(int(purchase.buyer), order_id=purchase.id)
    await bot.send_message(chat_id=ADMINS[0], text=order_info, reply_markup=keyboard_for_admins)
    await state.reset_state()
    await delete_cart(purchase.buyer)

    menu_keyboard = await menu_keyboards()
    await call.message.edit_text(text= f'Ваш заказ:\n'
                                       f'{item_name}\n'
                                       f'К оплате: {total_amount} руб.',

                                 )

    await call.message.answer(text=f'Ваш заказ №{purchase.id} принят в обработку!',
                              reply_markup=menu_keyboard)

# Ловим callback от нажатия кнопки принять от админа и отправляем пользователю статус заказа
@dp.callback_query_handler(support_callback.filter())
async def accept_order(call: CallbackQuery, callback_data: dict):
    order_id = callback_data.get('order_id')
    order = await get_order(int(order_id))
    user_id = callback_data.get('user_id')

    if order.delivery_method == 'Доставка':
        order_info = 'Получен заказ!\n' \
                     f'👤 Имя заказчика: {order.receiver}\n' \
                     f'🔑 ID пользователя: {order.buyer}\n' \
                     f'☎ Номер телефона: {order.phone_number}\n' \
                     f'🚚 Адрес доставки: {order.shipping_address}\n' \
                     f'🛎 Заказ:\n' \
                     f'{order.item_name}\n' \
                     f'💵 Сумма заказа: {order.amount} руб\n' \
                     f'💵 Сумма доставки: 100 руб\n' \
                     f'💰 Итоговая сумма: {order.amount + 100} руб\n'\
                     f'📜 Примечание к заказу:\n ' \
                     f'{order.note}'

    else:
        order_info = f'Получен заказ №{order.id}!\n' \
                     f'👤 Имя заказчика: {order.receiver}\n' \
                     f'🔑 ID пользователя: {order.buyer}\n' \
                     f'☎ Номер телефона: {order.phone_number}\n' \
                     f'🚚 Способ доставки: {order.delivery_method}\n' \
                     f'🛎 Заказ:\n' \
                     f'{order.item_name}\n' \
                     f'💰 Сумма заказа: {order.amount} руб\n' \
                     f'📜 Примечание к заказу:\n ' \
                     f'{order.note}'

    keyboard_ready = ready_keyboard(user_id, int(order_id))
    await call.message.edit_text(text=order_info, reply_markup=keyboard_ready)
    await call.bot.send_message(chat_id=user_id, text='Статус заказа: Готовится!')


@dp.callback_query_handler(ready_button_callback.filter())
async def send_ready_command(call: CallbackQuery, callback_data: dict):
    order_id = callback_data.get('order_id')
    order = await get_order(int(order_id))
    user_id = callback_data.get('user_id')

    if order.delivery_method == 'Доставка':
        order_info = f'🛎 Заказ № {order_id} Готов\n' \
                     f'👤 Имя заказчика: {order.receiver}\n' \
                     f'🔑 ID пользователя: {order.buyer}\n' \
                     f'☎ Номер телефона: {order.phone_number}\n' \
                     f'🚚 Адрес доставки: {order.shipping_address}\n' \
                     f'🛎 Заказ:\n' \
                     f'{order.item_name}\n' \
                     f'💵 Сумма заказа: {order.amount} руб\n' \
                     f'💵 Сумма доставки: 100 руб\n' \
                     f'💰 Итоговая сумма: {order.amount + 100} руб\n' \
                     f'📜 Примечание к заказу:\n ' \
                     f'{order.note}'
    else:
        order_info = f'Заказ №{order_id} Готов!\n' \
                     f'👤 Имя заказчика: {order.receiver}\n' \
                     f'🔑 ID пользователя: {order.buyer}\n' \
                     f'☎ Номер телефона: {order.phone_number}\n' \
                     f'🚚 Способ доставки: {order.delivery_method}\n' \
                     f'🛎 Заказ:\n' \
                     f'{order.item_name}\n' \
                     f'💰 Сумма заказа: {order.amount} руб\n' \
                     f'📜 Примечание к заказу:\n ' \
                     f'{order.note}'

    await call.message.edit_text(text=order_info)
    if order.delivery_method == 'Доставка':
        await call.bot.send_message(chat_id=user_id, text=f'Статус заказа {order.id}: Готов! Ожидайте доставку!')
    else:
        await call.bot.send_message(chat_id=user_id, text=f'Статус заказа {order.id}: Готов!')
    await call.bot.send_sticker(chat_id=user_id, sticker='CAACAgIAAxkBAAELJU5hCkFXMFQ4GokhJZrMBiZePzw4hwACHQADFkJrCoaz3LxWR4WIIAQ')
# При желании можно подключить собственную платежную систему Telegram
'''
@dp.callback_query_handler(text_contains='payment', state=states.NewItem.Approval)
async def approval(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Для оплаты нажмите "Заплатить" ')


    data = await state.get_data()

    purchase: models.PurchaseItem = data.get('purchase')
    items: models.Item = data.get('item')
    photo = await get_photo(items.name)


    await models.ShoppingCart.create(
        user_id=call.from_user.id,
        item_id=data.get('item_id'),
        item_name=purchase.item_name,
        quantity=data.get('amount') / data.get('item_price'),
        amount=data.get('amount')
    )
    user_id = purchase.buyer
    shopping_cart = await get_items_from_shipping_cart(user_id)
    item_name = []
    total_amount = 0
    for item in shopping_cart:
        item_name.append((str(item.item_name) + ' - ' + str(item.quantity) +'/шт'))
        total_amount+=item.amount

    item_name = ', '.join(item_name)

    currency = 'RUB'
    need_name = True
    need_phone_number = True
    need_email = False
    need_shipping_address = True

    await bot.send_invoice(
        call.message.chat.id,
        title='Ваш заказ:',
        description=item_name,
        payload='some-invoice-payload-for-our-internal-use',
        start_parameter='example',
        currency=currency,
        photo_url='https://imgv3.fotor.com/images/homepage-feature-card/Fotor-AI-photo-enhancement-tool-ru.jpg',
        photo_height=512,
        photo_width=512,
        photo_size=512,
        prices=PRICES,
        provider_token=LP_TOKEN,
        need_name=need_name,
        need_phone_number=need_phone_number,
        need_email=need_email,
        is_flexible=True,
        #need_shipping_address=need_shipping_address

    )
    cancel_button = InlineKeyboardButton(
        text='Отменить покупку',
        callback_data='cancel'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [cancel_button]
        ]
    )
    await call.message.answer(text='Отменить:',reply_markup=markup)
    await state.update_data(purchase=models.PurchaseItem(
        buyer = call.from_user.id,
        item_name=item_name,
        amount=total_amount,
        purchase_time=datetime.datetime.now(),
    ))
    await states.NewItem.Purchase.set()



@dp.pre_checkout_query_handler(state=states.NewItem.Purchase)
async def checkout(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, True)
    data = await state.get_data()
    purchase: models.PurchaseItem = data.get('purchase')
    success = await check_payment(purchase)
    if success:
        await purchase.create()
        await purchase.update(
            successful=True,
            shipping_address=pre_checkout_query.order_info.shipping_address.to_python()
            if pre_checkout_query.order_info.shipping_address
            else None,
            phone_number = pre_checkout_query.order_info.phone_number,
            receiver = pre_checkout_query.order_info.name,
        ).apply()

        await state.reset_state()
        await delete_cart(purchase.buyer)
        await bot.send_message(pre_checkout_query.from_user.id,
                               'Платеж на сумму {amount} RUB совершен успешно!!!'.format(
                                   amount=purchase.amount))

    else:
        await bot.send_message(pre_checkout_query.from_user.id,
                               'Покупка не была подтверждена, попробуйте позже....')
'''
@dp.message_handler()
async def other_echo(message: types.Message):
    await message.answer(message.text)


#async def check_payment(purchase: models.PurchaseItem):
 #   return True