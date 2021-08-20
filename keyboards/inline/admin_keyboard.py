from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData


support_callback = CallbackData("support", "user_id","order_id")
ready_button_callback = CallbackData("ready", "user_id", "order_id")

def order_for_admins(user_id, order_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Принять заказ',
            callback_data=support_callback.new(
                user_id=user_id,
                order_id=order_id
            )
        )
    )

    return markup

def ready_keyboard(user_id, order_id):
    keyboard_ready = InlineKeyboardMarkup()
    keyboard_ready.insert(
        InlineKeyboardButton(
            text='Заказ Готов!',
            callback_data=ready_button_callback.new(user_id, order_id)
        )
    )
    return keyboard_ready

async def cancel_button():
    cancel_btn = InlineKeyboardMarkup()
    cancel_btn.row(
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel'
        )
    )
    return cancel_btn

async def confirm_price():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Принять',
            callback_data='price_confirm'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Ввести заново',
            callback_data='price_change'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        )
    )
    return markup

async def confirm_weight():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Принять',
            callback_data='confirm_weigth'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Ввести заново',
            callback_data='weight_change'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        )
    )
    return markup
async def change_item():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.insert(KeyboardButton('➕ Создать новый товар'))
    keyboard.insert(KeyboardButton('❌ Удалить товар'))
    keyboard.insert(KeyboardButton('🔧 Изменить товар'))
    keyboard.row(KeyboardButton('↩ Вернуться'))

    return keyboard
async def transliterator(name):
    dict = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
              'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
              'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
              '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
              ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
              '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
              'Є': 'e', '—': ''}
    for key in dict:
        name = name.replace(key, dict[key])
    return name

async def choose_message_type():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        text='Рассылка с фото',
        callback_data='photo_mailing'

    )
    )
    markup.row(
        InlineKeyboardButton(
            text='Текстовое сообщение',
            callback_data='text_mailing'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='back_to_the_menu'
        )
    )
    return markup

async def photo_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        text='Принять',
        callback_data='accept_photo'

    )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_mailing'
        )
    )
    return markup

async def text_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        text='Принять',
        callback_data='accept_text'

    )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_mailing'
        )
    )
    return markup

async def item_change_menu():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Изменить цену',
            callback_data='item_change_price'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Изменить вес',
            callback_data='item_change_weight',
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Изменить описание',
            callback_data='item_change_description'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Изменить фото',
            callback_data='change_photo_command'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel_command'
        )
    )

    return markup

async def confirm_price_changes():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Подтвердить изменения',
            callback_data='ConfirmChangesPrice'
        )
    )

    markup.row(
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel_command'
        )
    )

    return markup
async def confirm_weight_changes():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Подтвердить изменения',
            callback_data='ConfirmWeightChanges'
        )
    )

    markup.row(
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel_command'
        )
    )

    return markup

async def confirm_description_changes():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Подтвердить изменения',
            callback_data='ConfirmDescChanges'
        )
    )

    markup.row(
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel_command'
        )
    )

    return markup

async def confirm_photo_changes():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Подтвердить изменения',
            callback_data='ConfirmPhotoChanges'
        )
    )

    markup.row(
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel_command'
        )
    )

    return markup

async def cancel_delete():
    markup = InlineKeyboardMarkup()

    markup.insert(
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel_delete'
        )
    )
    return markup