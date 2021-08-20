
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


from utils.db_api.db_commands import count_items, get_categories, get_items, get_subcategories, \
    get_items_with_subcategory

# Создаем Callbackdata - объекты, которые будут нужны для работы с меню
menu_cd = CallbackData('show_menu','level', 'category','subcategory', 'item_id')
buy_item = CallbackData('buy', 'item_id')

# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости
# от переданных параметров. Если подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, category="0",subcategory="0", item_id="0"):
    return menu_cd.new(level=level, category=category,subcategory=subcategory, item_id=item_id)


# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def categories_keyboard():
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup()

    # Забираем список товаров из базы данных с РАЗНЫМИ категориями и проходим по нему
    categories = await get_categories()
    for category in categories:
        # Чекаем в базе сколько товаров существует под данной категорией
        number_of_items = await count_items(category.category_code)

        # Сформируем текст, который будет на кнопке
        button_text = f"{category.category_name}"

        # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code)

        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Возвращаем созданную клавиатуру в хендлер
    return markup
async def subcategories_keyboard(category):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    # Забираем список товаров с РАЗНЫМИ подкатегориями из базы данных с учетом выбранной категории и проходим по ним
    subcategories = await get_subcategories(category)
    for subcategory in subcategories:
        print(subcategory.category_name)
        # Чекаем в базе сколько товаров существует под данной подкатегорией
        number_of_items = await count_items(category_code=category, subcategory_code=subcategory.subcategory_code)

        # Сформируем текст, который будет на кнопке
        button_text = f"{subcategory.subcategory_name} "

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, subcategory=subcategory.subcategory_code)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text='↩ Назад',
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1,
                category=category,
            )
        )
    )
    return markup
# Создаем функцию, которая отдает клавиатуру с доступными товарами, исходя из выбранной категории и подкатегории
async def items_keyboard(category, subcategory):
    if category == 'Sushi':
        CURRENT_LEVEL = 2
    else:
        CURRENT_LEVEL = 1

    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на товар
    markup = InlineKeyboardMarkup(row_width=2)

    # Забираем список товаров из базы данных с выбранной категорией и подкатегорией, и проходим по нему
    if category == 'Sushi':
        items = await get_items_with_subcategory(category, subcategory)
    else:
        items = await get_items(category)
    for item in items:
        # Сформируем текст, который будет на кнопке
        button_text = f"{item.name} - {item.price} руб."

        # Сформируем колбек дату, которая будет на кнопке
        if category == 'Sushi':
            callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                               category=category,
                                               subcategory=subcategory,
                                               item_id=item.id)
        else:
            callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                               category=category,
                                               item_id=item.id)
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 1 - на выбор подкатегории
    if category == 'Sushi':
        markup.row(
            InlineKeyboardButton(
                text="↩ Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                 category=category,
                                                 subcategory=subcategory)
            )
        )
    else:
        markup.row(
            InlineKeyboardButton(
                text="↩ Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                 category=category))
        )
    return markup

# Создаем функцию которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товарами
def item_keyboard(category, subcategory, item_id):
    if category == 'Sushi':
        CURRENT_LEVEL = 3
    else:
        CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Ввести количество товара",
            callback_data=buy_item.new(item_id=item_id)
        )
    )
    if category == 'Sushi':
        markup.row(
            InlineKeyboardButton(
                text="↩ Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                 category=category,
                                                 subcategory=subcategory)))
    else:
        markup.row(
            InlineKeyboardButton(
                text="↩ Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                 category=category
                                                 )))
    return markup

async def menu_keyboards():
    menu_button = KeyboardButton(text='🍴 Меню')
    cart_button = KeyboardButton(text='🛒 Корзина')
    markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).row(menu_button,cart_button)
    return markup

async def input_keyboard():
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
        button1, button2, button3,
        button4, button5, button6,
        button7, button8, button9
    )
    return num_keyboard

async def delivery_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        text='Оформить доставку - 100 руб', callback_data='delivery')

    )
    markup.row(
        InlineKeyboardButton(
            text='Забрать самому', callback_data='phone_number_pickup'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отменить заказ',
            callback_data='cancel'
        )
    )
    return markup

async def shipping_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Принять',
            callback_data='phone'
        )
    )
    markup.row(
        InlineKeyboardButton(
        text='Ввести заново',
            callback_data='change_shipping_address'
    )
    )
    return markup
async def phoneNumber_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Принять',
            callback_data='pickup'
        )
    )
    markup.row(
        InlineKeyboardButton(
        text='Ввести новый номер телефона',
        callback_data='phone'
    )
    )
    return markup
