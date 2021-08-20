import os


import logging

import asyncio
from asyncio import sleep

from data.config import ADMINS
from loader import bot
from utils.db_api.database import create_db

# Используем эту фукцию, чтобы заполнить базу данных товарами
from utils.db_api.db_commands import get_all_items
from utils.db_api.models import Item, Photo


async def add_items():
    await Item.create(name='Четыре сыра',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=400,description='• Моцарелла 🧀\n'
                                         '• томатный соус 🍛\n'
                                         '• Дор Блю 🧀\n'
                                         '• пармезан 🧀\n'
                                         '• гауда 🧀',
                   weight=820
                      )

    await Item.create(name='Пеперони',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=350, description='• Пикантная пепперони 🍕\n'
                                          '• моцарелла 🧀\n'
                                          '• томатный соус 🍛',
                      weight=350
                   )
    await Item.create(name='Четыре сезона',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=400, description='• Ветчина 🥩\n'
                                          '• моцарелла 🧀\n'
                                          '• пеперони🍕\n'
                                          '• грибы 🍈\n'
                                          '• помидоры 🍅\n'
                                          '• томатный соус 🍛',
                      weight=740
                   )
    await Item.create(name='Ветчина и грибы',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=370, description='• Ветчина 🥩\n'
                                          '• шампиньоны \n'
                                          '• моцарелла 🧀\n'
                                          '• томатный соус 🍅',
                      weight=790

                   )
    await Item.create(name='Ветчина и сыр',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=370, description='• Ветчина 🥩\n'
                                          '• моцарелла 🧀\n'
                                          '• томатный соус 🍛',
                      weight=740

                   )
    await Item.create(name='Маргарита',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=330, description='• Моцарелла 🧀\n'
                                          '• помидор 🧀\n'
                                          '• итальянские травы 🥬\n'
                                          '• томатный соус 🍛',
                      weight=740
                   )
    await Item.create(name='С лососем',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=450, description='• Филе лосося 🐟\n'
                                          '• зелень 🥗\n'
                                          '• сливочный соус 🍛\n'
                                          '• маслины 🫒\n'
                                          '• моцарелла 🧀\n'
                                          '• помидор 🍅',
                      weight=740
                   )
    await Item.create(name='Ассорти',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=420, description='• Ветчина 🥩\n'
                                          '• копченая колбаса 🥩\n'
                                          '• курица 🐔\n'
                                          '• помидор 🍅\n'
                                          '• томатный соус 🍲',
                      weight=790

                   )
    await Item.create(name='Мясная',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=450, description='• Моцарелла 🧀\n'
                                          '• копченая колбаска 🥩\n'
                                          '• ветчина 🥩\n'
                                          '• пеперони 🍕\n'
                                          '• охотничьи колбаски 🥩\n'
                                          '• томатный соус 🍛',
                      weight=740
                   )
    await Item.create(name='Маринара',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=450, description='• Креветки 🍤\n'
                                          '• моцарелла 🧀\n'
                                          '• томатный соус 🍛\n'
                                          '• помидор 🍅',
                      weight=740
                   )
    await Item.create(name='С копченкой',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=370, description='• Копченые колбаски 🥩\n'
                                          '• помидор 🍅\n'
                                          '• моцарелла 🧀\n'
                                          '• томатный соус 🍛 ',
                      weight=790
                   )
    await Item.create(name='Пан чикен',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=400, description='• Моцарелла 🧀\n'
                                          '• помидор 🍅\n'
                                          '• курица 🐔\n'
                                          '• маринованный огурец 🥒\n',
                      weight=740

                   )
    await Item.create(name='Болоньезе',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=450, description='• Фарш говядина 🥩\n'
                                          '• лук красный 🧅\n'
                                          '• моцарелла 🧀\n'
                                          '• помидор 🍅\n',
                      weight=740
                   )
    await Item.create(name='Карбонара',
                   category_name='🍕 Пицца', category_code='Pizza',
                   subcategory_name='-', subcategory_code='-',
                   price=400, description='• Бекон 🥓\n'
                                          '• моцарелла 🧀\n'
                                          '• лук 🧅\n'
                                          '• сливочный соус 🍛\n'
                                          '• итальянские травы 🥬',
                      weight=820
                   )

    await Item.create(name='Шаурма №1',
                   category_name='🌯 Шаурма', category_code='Shaurma',
                   subcategory_name='-', subcategory_code='-',
                   price=140, description='• Сочная курочка 🐔\n'
                                          '• пекинская капуста 🥬\n'
                                          '• маринованные огурчики 🥒\n'
                                          '• помидор 🍅\n'
                                          '• фирменный соус 🍛',
                      weight=450
                   )
    await Item.create(name='Шаурма №2',
                   category_name='🌯 Шаурма', category_code='Shaurma',
                   subcategory_name='-', subcategory_code='-',
                   price=140, description='- Сочная курочка 🐔\n'
                                          '- пекинская капуста 🥬\n'
                                          '- свежие огурчики 🥒\n '
                                          '- помидор 🍅\n'
                                          '- фирменный соус 🍛',
                      weight=450
    )
    await Item.create(name='Шаурма №3',
                   category_name='🌯 Шаурма', category_code='Shaurma',
                   subcategory_name='-', subcategory_code='-',
                   price=140, description='• Сочная курочка 🐔\n'
                                          '• морковь по-корейски 🥕\n'
                                          '• пекинская капуста 🥬\n'
                                          '• помидор 🍅\n'
                                          '• фирменный соус 🍛',
                      weight=450

                   )

    await Item.create(name='Сиро',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name = 'Фирменные роллы', subcategory_code = 'branded_rolls',
                      price=250, description='• угорь 🥩 \n'
                                             '• лосось 🐟\n'
                                             '• креветка 🍤\n'
                                             '• огурец 🥒\n'
                                             '• майонез 🍛',
                      weight=250

                      )
    await Item.create(name='Филадельфия',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• лосось 🐟\n'
                                             '• сыр 🧀 ',

                      weight=250

                      )
    await Item.create(name='Филадельфия с огурцом',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒',

                      weight=250

                      )
    await Item.create(name='Филадельфия c креветкой',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• лосось 🐟\n'
                                             '• креветка 🍤\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒',

                      weight=250

                      )
    await Item.create(name='Филадельфия с красной икрой',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=280, description='• лосось 🐟\n'
                                             '• кр. икра 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• зел. лук 🧅 ',

                      weight=250

                      )
    await Item.create(name='Калифорния',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=180, description='• Краб 🦀\n'
                                             '• тобико оранж 🍛\n'
                                             '• майонез 🥣\n'
                                             '• огурец 🥒\n',

                      weight=250

                      )
    await Item.create(name='Калифорния с угрем',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• угорь 🥩 \n'
                                             '• тобико оранж 🍣\n'
                                             '• майонез 🍛\n'
                                             '• огурец 🥒',

                      weight=220

                      )
    await Item.create(name='Калифорния c лососем',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• лосось 🐟\n'
                                             '• тобико оранж 🍣\n'
                                             '• майонез 🍛\n'
                                             '• огурец 🥒',

                      weight=220

                      )
    await Item.create(name='Калифорния с креветкой',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• креветка 🍤\n'
                                             '• тобико оранж 🍣\n'
                                             '• майонез 🍛\n'
                                             '• огурец 🥒',

                      weight=220

                      )
    await Item.create(name='Калифорния микс',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• креветка 🍤\n'
                                             '• угорь 🥩 \n'
                                             '• тобико оранж 🍣\n'
                                             '• майонез 🍛\n'
                                             '• огурец 🥒',

                      weight=230

                      )
    await Item.create(name='Канада',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• угорь 🥩 \n'
                                             '• тобико кр 🍣\n'
                                             '• унаги соус 🍛\n'
                                             '• кунжут ㊙',

                      weight=250

                      )
    await Item.create(name='Канада с лососем',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• угорь 🥩 \n'
                                             '• лосось 🐟\n'
                                             '• унаги соус 🍛\n'
                                             '• кунжут ㊙',

                      weight=250

                      )
    await Item.create(name='Канада лайт',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• угорь 🥩 \n'
                                             '• огурец 🥒\n'
                                             '• сыр 🧀 \n'
                                             '• унаги соус 🍛\n'
                                             '• кунжут ㊙',

                      weight=250

                      )
    await Item.create(name='Канада с креветкой',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=300, description='• угорь 🥩 \n'
                                             '• креветка 🍤\n'
                                             '• сыр 🧀 \n'
                                             '• тобико кр 🍣\n'
                                             '• унаги соус 🍛\n'
                                             '• кунжут ㊙',

                      weight=250

                      )
    await Item.create(name='Дуэт',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• угорь 🥩 \n'
                                             '• лосось 🐟\n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n',

                      weight=230

                      )
    await Item.create(name='Русский',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=180, description='• Курица 🐔\n'
                                             '• сыр 🧀 \n'
                                             '• укроп 🥦\n'
                                             '• огурец 🥒\n',

                      weight=220

                      )
    await Item.create(name='Касатка',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=200, description='• Окунь 🐟\n'
                                             '• лосось 🐟\n'
                                             '• кунжут микс ㊙\n'
                                             '• майонез 🍛\n'
                                             '• огурец 🥒',

                      weight=220

                      )
    await Item.create(name='Сиам',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=200, description='• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• тобико кр 🍣\n'
                                             '• паприка 🌶',

                      weight=220

                      )
    await Item.create(name='Камикадзе',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=290, description='• лосось 🐟\n'
                                             '• угорь 🥩 \n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒',

                      weight=250

                      )
    await Item.create(name='Тоторо',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=270, description='• огурец 🥒\n'
                                             '• сыр 🧀 \n'
                                             '• лосось 🐟\n'
                                             '• кунжут черный ㊙\n'
                                             '• зел. лук 🧅\n'
                                             '• краб 🦀',

                      weight=250

                      )
    await Item.create(name='Сливочная креветка',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=300, description='• сыр 🧀 \n'
                                             '• лосось 🐟\n'
                                             '• огурец 🥒\n'
                                             '• масага 🐟'
                                             '• креветка 🍤\n',

                      weight=280

                      )
    await Item.create(name='Банзай',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• огурец 🥒\n'
                                             '• сыр 🧀 \n'
                                             '• креветка 🍤\n'
                                             '• масаго оранжевая 🐟',

                      weight=250

                      )
    await Item.create(name='Пирамида',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=300, description='• лосось 🐟\n'
                                             '• угорь 🥩 \n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒\n'
                                             '• масага🐟',

                      weight=230

                      )
    await Item.create(name='Сэндвич',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=280, description='• сыр 🧀 \n'
                                             '• лосось 🐟\n'
                                             '• огурец 🥒',

                      weight=250

                      )
    await Item.create(name='Фьюжн',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=220, description='• угорь 🥩 \n'
                                             '• кунжут микс ㊙\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒',


                      weight=220

                      )
    await Item.create(name='Киота',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• тобико кр 🍣\n'
                                             '• тунец 🐟',

                      weight=220

                      )
    await Item.create(name='Овощной',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=150, description='• паприка 🌶\n'
                                             '• помидор 🍅\n'
                                             '• салат 🥬\n'
                                             '• огурец 🥒',

                      weight=250

                      )
    await Item.create(name='Фуджи',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=220, description='• курица 🐔\n'
                                             '• угорь 🥩\n'
                                             '• огурец 🥒\n'
                                             '• кунжут ㊙\n'
                                             '• сыр 🧀 ',

                      weight=240

                      )
    await Item.create(name='Нота с лососем',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒\n'
                                             '• кунжут ㊙',

                      weight=230

                      )
    await Item.create(name='Цезарь',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=180, description='• курица 🐔\n'
                                             '• сыр 🧀 \n'
                                             '• помидор 🍅\n'
                                             '• салат 🥬\n'
                                             '• кунжут ㊙',

                      weight=230

                      )
    await Item.create(name='Сайко',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• креветка 🍤\n'
                                             '• соус спайси 🍛\n'
                                             '• огурец 🥒\n'
                                             '• кунжут ㊙\n'
                                             '• сыр 🧀 ',

                      weight=230

                      )
    await Item.create(name='Окинава',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=240, description='• угорь 🥩 \n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒\n'
                                             '• кунжут ㊙',

                      weight=230

                      )
    await Item.create(name='Кани тортилья',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=200, description='• краб 🦀\n'
                                             '• сыр 🧀 \n'
                                             '• помидор 🍅\n'
                                             '• салат 🥬',


                      weight=180

                      )
    await Item.create(name='Эби тортилья',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• креветка 🍤\n'
                                             '• сыр 🧀 \n'
                                             '• помидор 🍅\n'
                                             '• салат 🥬',


                      weight=180

                      )
    await Item.create(name='Сяке тортилья',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• лосось 🐟\n'
                                             '• сыр 🧀\n'
                                             '• помидор 🍅\n'
                                             '• салат 🥬',

                      weight=180

                      )
    await Item.create(name='Тори тортилья',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=200, description='• курица 🐔\n'
                                             '• сыр 🧀 \n'
                                             '• помидор 🍅\n'
                                             '• салат 🥬',

                      weight=180

                      )
    await Item.create(name='Унаги тортилья',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• угорь 🥩 \n'
                                             '• сыр 🧀 \n'
                                             '• помидор 🍅\n'
                                             '• салат 🥬',

                      weight=180

                      )
    await Item.create(name='Нежный люкс',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• тунец 🐟\n'
                                             '• лосось 🐟\n'
                                             '• огурец 🥒\n'
                                             '• соус спайси 🍛\n'
                                             '• стружка тунца 🐟',

                      weight=220

                      )
    await Item.create(name='Нежный с лососем',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒\n'
                                             '• стружка тунца 🐟',

                      weight=230
                      )
    await Item.create(name='Нежный с тунцом',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=260, description='• тунец 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒\n'
                                             '• стружка тунца 🐟',

                      weight=230
                      )
    await Item.create(name='Сытный',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=300, description='• креветка 🍤\n'
                                             '• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒',


                      weight=250
                      )
    await Item.create(name='Катана',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• креветка 🍤\n'
                                             '• тобико оранж 🍛\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒',

                      weight=230
                      )
    await Item.create(name='Ямато',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• креветка 🍤\n'
                                             '• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒',

                      weight=230
                      )
    await Item.create(name='Блэк',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• тобико оранж 🍛\n'
                                             '• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• огурец 🥒',

                      weight=230
                      )
    await Item.create(name='Банкок',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• икра лос. 🐟\n'
                                             '• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• краб 🦀\n'
                                             '• огурец 🥒',

                      weight=240
                      )
    await Item.create(name='Тако маки',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=250, description='• угорь 🥩 \n'
                                             '• лосось 🐟\n'
                                             '• сыр 🧀 \n'
                                             '• тобико кр 🍣',

                      weight=240
                      )
    await Item.create(name='Симаки',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Фирменные роллы', subcategory_code='branded_rolls',
                      price=230, description='• угорь 🥩 \n'
                                             '• такуан 🧈\n'
                                             '• сыр 🧀 \n'
                                             '• тобико кр 🍣',

                      weight=230
                      )
    await Item.create(name='Огурец',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=50, description='• огурец 🥒\n'
                                             '• кунжут ㊙\n',

                      weight=115
                      )
    await Item.create(name='Кани',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=80, description='• краб 🦀\n',

                      weight=115
                      )
    await Item.create(name='Чука',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=80, description='• Водоросли чука 🌱\n',

                      weight=115
                      )
    await Item.create(name='Такуан',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=80, description='• Такуан 🧈 ',

                      weight=115
                      )
    await Item.create(name='Тэка',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=140, description='• тунец 🐟',

                      weight=115
                      )
    await Item.create(name='Эби',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=150, description='• креветка 🍤',

                      weight=115
                      )
    await Item.create(name='Икура',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=150, description='• икра лос. 🐟\n'
                                             '• сыр 🧀 ',

                      weight=120
                      )
    await Item.create(name='Тори',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=120, description='• курица 🐔\n'
                                             '• соус спайси 🍛\n'
                                             '• помидор 🍅\n'
                                             '• салат 🥬',

                      weight=170
                      )
    await Item.create(name='Лосось терияки',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=100, description='• лосось 🐟\n'
                                             '• соус терияки 🍛',

                      weight=115
                      )
    await Item.create(name='Ясай',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=120, description='• паприка 🌶\n'
                                             '• помидор 🍅\n'
                                             '• огурец 🥒\n'
                                             '• салат 🥬\n'
                                             '• майонез 🍛',

                      weight=170
                      )
    await Item.create(name='Микадо',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=120, description='• лосось 🐟\n'
                                             '• огурец 🥒',

                      weight=115
                      )
    await Item.create(name='Умаджи',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=150, description='• угорь 🥩 \n'
                                             '• огурец 🥒\n'
                                             '• унаги соус🍛\n'
                                             '• кунжут ㊙',

                      weight=120
                      )
    await Item.create(name='Макеши',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Классические роллы', subcategory_code='classic_rolls',
                      price=130, description='• лосось 🐟\n'
                                             '• зел. лук 🧅\n'
                                             '• соус спайси 🍛',

                      weight=115
                      )
    # Горячие роллы
    await Item.create(name='Унаги хот',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=250, description='• угорь 🥩 \n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• тобико кр 🍣',

                      weight=270
                      )
    await Item.create(name='Сяки хот',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=250, description='• креветка 🍤\n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• тобико кр 🍣',


                      weight=270
                      )
    await Item.create(name='Тэка хот',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=260, description='• тунец 🐟\n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒',

                      weight=270
                      )
    await Item.create(name='Мадагаскар',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=240, description='• угорь 🥩 \n'
                                             '• огурец 🥒\n'
                                             '• краб 🦀\n'
                                             '• соус спайси 🍛',


                      weight=270
                      )
    await Item.create(name='Эби темпура',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=250, description='• креветки 🍤\n'
                                             '• огурец 🥒\n'
                                             '• помидор 🍅\n'
                                             '• сыр 🧀\n'
                                             '• салат 🥬',

                      weight=270
                      )
    await Item.create(name='Икура маки',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=250, description='• лосось 🐟\n'
                                             '• огурец 🥒\n'
                                             '• сыр 🧀\n'
                                             '• икра лососевая 🐟\n',

                      weight=270
                      )
    await Item.create(name='Якудза',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=240, description='• лосось 🐟\n'
                                             '• краб 🦀\n'
                                             '• огурец 🥒\n'
                                             '• соус спайси 🍛',

                      weight=270
                      )
    await Item.create(name='Яки нику',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=230, description='• угорь 🥩 \n'
                                             '• огурец 🥒\n'
                                             '• курица 🐔\n'
                                             '• сыр 🧀',

                      weight=270
                      )
    await Item.create(name='Сяки темпура',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=230, description='• лосось 🐟\n'
                                             '• огурец 🥒\n'
                                             '• тобико кр 🍣\n'
                                             '• сыр 🧀',


                      weight=270
                      )
    await Item.create(name='Запад',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=200, description='• курица 🐔\n'
                                             '• огурец 🥒\n'
                                             '• помидор 🍅\n'
                                             '• тобико кр 🍣\n'
                                             '• майонез 🍛',

                      weight=270
                      )
    await Item.create(name='Калифорния темпура',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=200, description='• краб 🦀\n'
                                             '• тобико кр 🍣\n'
                                             '• огурец 🥒\n'
                                             '• майонез 🍛',

                      weight=270
                      )
    await Item.create(name='Токио',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=300, description='• угорь 🥩 \n'
                                             '• лосось 🐟\n'
                                             '• креветки 🍤\n'
                                             '• огурец 🥒\n'
                                             '• сыр 🧀',

                      weight=290
                      )
    await Item.create(name='Умэ',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=300, description='• тунец 🐟\n'
                                             '• окунь 🐟\n'
                                             '• лосось 🐟\n'
                                             '• огурец 🥒\n'
                                             '• сыр 🧀',

                      weight=270
                      )
    await Item.create(name='Сафари',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=270, description='• угорь 🥩 \n'
                                             '• окунь 🐟\n'
                                             '• огурец 🥒\n'
                                             '• сыр 🧀',

                      weight=270
                      )
    await Item.create(name='Сяки терияки',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Горячие роллы', subcategory_code='hot_rolls',
                      price=220, description='• лосось терияки 🐟\n'
                                             '• спайси 🍛\n'
                                             '• пекинка 🥬\n',


                      weight=270
                      )
    # Запеченные роллы
    await Item.create(name='Сансей',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=180, description='• кунжут черный ㊙\n'
                                             '• соус спайси 🍛\n'
                                             '• помидор 🍅\n'
                                             '• краб 🦀\n',


                      weight=210
                      )
    await Item.create(name='Яки-Фурай',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=240, description='• лосось 🐟\n'
                                             '• краб 🦀\n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• соус спайси 🍛',

                      weight=250
                      )
    await Item.create(name='Яки-Магура',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=300, description='• тунец 🐟\n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• кунжут ㊙\n'
                                             '• соус спайси 🍛',

                      weight=250
                      )
    await Item.create(name='Яки-Хокайдо',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=260, description='• угорь 🥩 \n'
                                             '• лосось 🐟\n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• тобико 🍣\n'
                                             '• соус спайси 🍛',

                      weight=250
                      )
    await Item.create(name='Чикен-Чуз',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=180, description='• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• помидор 🍅\n'
                                             '• курица 🐔\n'
                                             '• кунжут ㊙\n'
                                             '• яки соус 🍛',

                      weight=210
                      )
    await Item.create(name='Филадельфия запеченная',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=270, description='• лосось 🐟\n'
                                             '• угорь 🥩 \n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• гауда 🧀',

                      weight=250
                      )
    await Item.create(name='Мидии',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=250, description='• Мидии 🦪\n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• яки соус 🍛',

                      weight=250
                      )
    await Item.create(name='Краб',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=250, description='• краб 🦀\n'
                                             '• угорь 🥩 \n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• яки соус 🍛',

                      weight=250
                      )
    await Item.create(name='Суши-Пицца',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Запеченные роллы', subcategory_code='baked_rolls',
                      price=270, description='• угорь 🥩 \n'
                                             '• сыр 🧀\n'
                                             '• моцарелла 🧀\n'
                                             '• яки соус 🍛',

                      weight=280
                      )
    #Премиум роллы
    await Item.create(name='Шеф Ролл',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Премиум роллы', subcategory_code='premium_rolls',
                      price=350, description='• лосось 🐟\n'
                                             '• угорь 🥩 \n'
                                             '• сыр 🧀\n'
                                             '• огурец 🥒\n'
                                             '• масага 🐟\n'
                                             '• креветка 🍤',

                      weight=320
                      )
    await Item.create(name='Сэйджи',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Премиум роллы', subcategory_code='premium_rolls',
                      price=350, description='• угорь 🥩 \n'
                                             '• креветка 🍤\n'
                                             '• огурец 🥒\n'
                                             '• сыр 🧀\n'
                                             '• масага 🐟',

                      weight=320
                      )
    await Item.create(name='Панда',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Премиум роллы', subcategory_code='premium_rolls',
                      price=350, description='• лосось 🐟\n'
                                             '• сыр 🧀\n'
                                             '• креветка 🍤\n'
                                             '• огурец 🥒\n'
                                             '• масага 🐟',

                      weight=320
                      )
    await Item.create(name='Радуга',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Премиум роллы', subcategory_code='premium_rolls',
                      price=350, description='• угорь 🥩 \n'
                                             '• лосось 🐟\n'
                                             '• тунец 🐟\n'
                                             '• сыр 🧀\n'
                                             '• масага 🐟\n'
                                             '• огурец 🥒\n',

                      weight=320
                      )
    #Сеты
    await Item.create(name='Сет 1',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=750, description='• Нежный с лососем 🍣\n'
                                             '• Калифорния 🍣\n'
                                             '• Канада 🍣\n'
                                             '• Сайко 🍣',


                      weight=940
                      )
    await Item.create(name='Сет 2',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=1050, description='• Филадельфия 🍣\n'
                                              '• Яки-Фурай 🍣\n'
                                              '• Симаки 🍣\n'
                                              '• Радуга 🍣\n'
                                              '• Эби 🍣',

                      weight=1110
                      )
    await Item.create(name='Сет 3',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=580, description='• Калифорния с лососем 🍣 \n'
                                             '• Цезарь 🍣\n'
                                             '• Сиро 🍣',


                      weight=670
                      )
    await Item.create(name='Сет 4',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=1000, description='• Калифорния Темпура 🍣\n'
                                              '• Нежный люкс 🍣\n'
                                              '• Филадельфия 🍣\n'
                                              '• Чикен-Чуз 🍣\n'
                                              '• Умаджи 🍣\n'
                                              '• Микадо 🍣\n'
                                              '• Огурец 🍣',

                      weight=1310
                      )
    await Item.create(name='Сет 5',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=600, description='• Филадельфия с огурцом 🍣\n'
                                             '• Канада лайт 🍣\n'
                                             '• Огурец 🍣\n'
                                             '• Такуан 🍣\n'
                                             '• Кани 🍣',

                      weight=860
                      )
    await Item.create(name='Сет 6',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=650, description='• Филадельфия запеченная 🍣 \n'
                                             '• Сансэй 🍣\n'
                                             '• Краб 🍣',

                      weight=720
                      )
    await Item.create(name='Сет 7',
                          category_name='🍣 Суши', category_code='Sushi',
                          subcategory_name='Сеты', subcategory_code='sets',
                          price=400, description='• Калифорния 🥩 \n'
                                                 '• Яки-Хокайдо 🍣\n'
                                                 '• Огурец 🍣',

                          weight=600
                          )
    await Item.create(name='Сет 8',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=650, description='• Сяки темпура 🍣\n'
                                             '• Эби хот 🍣\n'
                                             '• Унаги хот 🍣',


                      weight=840
                      )
    await Item.create(name='Сет 9',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=650, description='• Мидии 🍣 \n'
                                             '• Сансэй 🍣\n'
                                             '• Русский 🍣',

                      weight=750
                      )
    await Item.create(name='Сет DOS',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=2000, description='• Калифорния темпура 🍣\n'
                                              '• Кани Тортилья 🍣\n'
                                              '• Филадельфия 🍣\n'
                                              '• Мидии запеч. 🍣\n'
                                              '• Чикен-Чуз 🍣\n'
                                              '• Овощной 🍣\n'
                                              '• Микадо 🍣\n'
                                              '• Сафари 🍣\n'
                                              '• Огурец 🍣\n'
                                              '• Фуджи 🍣\n'
                                              '• Осака 🍣\n'
                                              '• Тэка 🍣',


                      weight=2500
                      )
    await Item.create(name='Запеченный Сет',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=1000, description='• Лосось 🐟\n'
                                              '• Креветка 🍤\n'
                                              '• Угорь 🥩 \n'
                                              '• Краб 🍣\n'
                                              '• Тунец 🐟',




                      weight=840
                      )
    await Item.create(name='Сет Праздничный',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=1500, description='• Филадельфия 🍣 \n'
                                             '• Калифорния 🍣\n'
                                             '• Окинава 🍣\n'
                                             '• Пирамида 🍣 \n'
                                             '• Банзай 🍣\n'
                                             '• Огурец 🍣\n'
                                             '• Эби 🍣 \n'
                                             '• Тэка 🍣',



                      weight=750
                      )
    await Item.create(name='Сет Ассорти',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Сеты', subcategory_code='sets',
                      price=1100, description='• Дуэт \n'
                                              '• Эби Хот 🍣\n'
                                              '• Сяке Терияки 🍣\n'
                                              '• Чикен-Чуз 🍣\n'
                                              '• Краб 🍣\n',


                      weight=2500
                      )
    # Бургеры
    await Item.create(name='Бургер 1',
                      category_name='🍔 Бургеры', category_code='burgers',
                      subcategory_name='-', subcategory_code='-',
                      price=160, description='• котлета 🥩\n'
                                              '• луковые кольца 🧅\n'
                                              '• помидор 🍅 \n'
                                              '• салат 🥬\n'
                                              '• соус BBQ 🍛',

                      weight=100
                      )
    await Item.create(name='Бургер 2',
                      category_name='🍔 Бургеры', category_code='burgers',
                      subcategory_name='-', subcategory_code='-',
                      price=180, description='• котлета 🥩\n'
                                              '• сырный соус 🧀\n'
                                              '• луковые кольца 🧅\n'
                                              '• бекон 🥓\n'
                                              '• сыр  🧀\n'
                                              '• кетчуп 🥫',

                      weight=100
                      )
    await Item.create(name='Бургер 3',
                      category_name='🍔 Бургеры', category_code='burgers',
                      subcategory_name='-', subcategory_code='-',
                      price=170, description='• котлета 🥩\n'
                                              '• острый соус 🍛\n'
                                              '• огурчик маринованный 🥒\n'
                                              '• сыр  🧀\n'
                                              '• паприка 🌶',


                      weight=100
                      )
    await Item.create(name='Бургер 4',
                      category_name='🍔 Бургеры', category_code='burgers',
                      subcategory_name='-', subcategory_code='-',
                      price=175, description='• котлета 🥩\n'
                                             '• сыр сливочный 🧀\n'
                                             '• помидор 🍅 \n'
                                             '• луковые кольца 🧅',

                      weight=100
                      )
    await Item.create(name='Бургер 5',
                      category_name='🍔 Бургеры', category_code='burgers',
                      subcategory_name='-', subcategory_code='-',
                      price=170, description='• котлета 🥩\n'
                                             '• соус терияки 🍛\n'
                                             '• помидор 🍅 \n'
                                             '• луковые кольца 🧅\n'
                                             '• салат 🥬\n'
                                             '• соус сметанный 🍛',

                      weight = 100

                      )
    # Вок лапша
    await Item.create(name='Удон с курицей',
                      category_name='🥡 Wok-Лапша', category_code='wok-noodles',
                      subcategory_name='-', subcategory_code='-',
                      price=170, description='• овощной микс 🥗\n'
                                             '• курица 🐔\n'
                                             '• лапша 🍝\n'
                                             '• соус терияки 🍛',

                      weight=100
                      )
    await Item.create(name='Удон с говядиной',
                      category_name='🥡 Wok-Лапша', category_code='wok-noodles',
                      subcategory_name='-', subcategory_code='-',
                      price=180, description='• овощной микс 🥗\n'
                                             '• говядина 🥩\n'
                                             '• лапша 🍝\n'
                                             '• соус терияки 🍛',

                      weight=100
                      )
    await Item.create(name='Удон со свининой',
                      category_name='🥡 Wok-Лапша', category_code='wok-noodles',
                      subcategory_name='-', subcategory_code='-',
                      price=180, description='• овощной микс 🥗\n'
                                             '• свинина 🥩\n'
                                             '• лапша 🍝\n'
                                             '• соус терияки 🍛',

                      weight=100
                      )
    await Item.create(name='Удон с креветкой',
                      category_name='🥡 Wok-Лапша', category_code='wok-noodles',
                      subcategory_name='-', subcategory_code='-',
                      price=220, description='• овощной микс 🥗\n'
                                             '• креветки 🍤\n'
                                             '• лапша 🍝\n'
                                             '• соус терияки 🍛',
                      weight=100
                      )
    await Item.create(name='Удон с угрем',
                      category_name='🥡 Wok-Лапша', category_code='wok-noodles',
                      subcategory_name='-', subcategory_code='-',
                      price=240, description='• овощной микс 🥗\n'
                                             '• угорь 🥩\n'
                                             '• лапша 🍝\n'
                                             '• соус терияки 🍛',
                      weight=100
                      )
    await Item.create(name='Удон с лососем',
                      category_name='🥡 Wok-Лапша', category_code='wok-noodles',
                      subcategory_name='-', subcategory_code='-',
                      price=200, description='• овощной микс 🥗\n'
                                             '• лосось 🐟\n'
                                             '• лапша 🍝\n'
                                             '• соус терияки 🍛',
                      weight=100
                      )
    await Item.create(name='Удон с овощами',
                      category_name='🥡 Wok-Лапша', category_code='wok-noodles',
                      subcategory_name='-', subcategory_code='-',
                      price=150, description='• овощной микс 🥗\n'
                                             '• лапша 🍝\n'
                                             '• соус терияки 🍛',
                      weight=100
                      )
    # Гунканы
    await Item.create(name='Спайси',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Гунканы', subcategory_code='gunkans',
                      price=70, description='• рыба в ассортименте 🐟',

                      weight=50
                      )
    await Item.create(name='Сырный',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Гунканы', subcategory_code='gunkans',
                      price=70, description='• рыба в ассортименте 🐟',

                      weight=50
                      )
    await Item.create(name='Икура',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Гунканы', subcategory_code='gunkans',
                      price=70, description='• Тобико в ассортименте 🐟',

                      weight=50
                      )
    # Суши
    await Item.create(name='Кальмар',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Суши', subcategory_code='sushi',
                      price=50, description='• Кальмар 🦑',

                      weight=35
                      )
    await Item.create(name='Тунец',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Суши', subcategory_code='sushi',
                      price=50, description='• Тунец 🐟',

                      weight=35
                      )
    await Item.create(name='Лосось',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Суши', subcategory_code='sushi',
                      price=50, description='• Лосось 🐟',

                      weight=35
                      )
    await Item.create(name='Окунь',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Суши', subcategory_code='sushi',
                      price=50, description='• Окунь 🐟',

                      weight=35
                      )
    await Item.create(name='Осьминог',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Суши', subcategory_code='sushi',
                      price=50, description='• осьминог 🐙',

                      weight=35
                      )
    await Item.create(name='Креветка',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Суши', subcategory_code='sushi',
                      price=50, description='• Креветка 🍤',

                      weight=35
                      )
    await Item.create(name='Угорь',
                      category_name='🍣 Суши', category_code='Sushi',
                      subcategory_name='Суши', subcategory_code='sushi',
                      price=50, description='• Угорь 🥩',

                      weight=35
                      )
    # Закуски
    await Item.create(name='Креветки Темпура',
                      category_name='🍟 Закуски', category_code='snaсks',
                      subcategory_name='-', subcategory_code='-',
                      price=250, description='• Креветки тампура 🍤',

                      weight=200
                      )
    await Item.create(name='Наггетсы(6шт)',
                      category_name='🍟 Закуски', category_code='snaсks',
                      subcategory_name='-', subcategory_code='-',
                      price=100, description='• Наггетсы - 6шт',

                      weight=100
                      )
    await Item.create(name='Наггетсы(10шт)',
                      category_name='🍟 Закуски', category_code='snaсks',
                      subcategory_name='-', subcategory_code='-',
                      price=150, description='• Наггетсы - 10 шт.',

                      weight=150
                      )
    await Item.create(name='Картофель Фри',
                  category_name='🍟 Закуски', category_code='snaсks',
                  subcategory_name='-', subcategory_code='-',
                  price=80, description='• Картофель Фри 🍟',

                  weight=150
                  )
    logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


async def items():
    name_items = []
    items = await get_all_items()
    for item in items:
        name_items.append(str(item.name))
    return name_items
loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_items())

BASE_MEDIA_PATH ='./media'

async def uploadPhoto():
    folders_name = await items()
    for folder in folders_name:
        method = bot.send_photo
        file_attr = 'photo'
        folder_path = os.path.join(BASE_MEDIA_PATH, folder)
        for filename in os.listdir(folder_path):
            if filename.startswith('.'):
                continue
            logging.info(f'Starting processing {filename}')
            with open(os.path.join(folder_path, filename), 'rb') as file:
                msg = await method(ADMINS[0], file, disable_notification=True)

                if file_attr == 'photo':
                    file_id = msg.photo[-1].file_id
                else:
                    file_id = getattr(msg, file_attr).file_id
                try:
                    await Photo.create(file_id=file_id, filename=filename, product=folder)
                except Exception as e:
                    logging.error(
                        'Couldn\'t upload {}. Error is {}'.format(filename, e)

                    )
                else:
                    logging.info(
                        f'Successfully uploaded and saved to DB file {filename} with id {file_id}'
                    )
        await sleep(0.3)

loop.run_until_complete(uploadPhoto())
''' task = [
    loop.create_task(uploadPhoto('Ветчина и грибы', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Ветчина и сыр', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Карбонара', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Маргарита', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Пеперони', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('С лососем', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Четыре сыра', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Четыре сезона', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Мясная', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('С копченкой', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Пан чикен', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Ассорти', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Болоньезе', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Маринара', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Шаурма №1', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Шаурма №2', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Шаурма №3', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сиро', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Канада с лососем', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Кани тортилья', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Касатка', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Катана', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Киота', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Нежный люкс', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Нежный с лососем', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Нежный с тунцом', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Нота с лососем', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Овощной', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Окинава', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Пирамида', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Русский', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сайко', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сиам', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Симаки', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сливочная креветка', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сытный', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сэндвич', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сяке тортилья', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Тако маки', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Тори тортилья', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Тоторо', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Унаги тортилья', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Филадельфия', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Филадельфия c креветкой', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Филадельфия с красной икрой', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Филадельфия с огурцом', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Фуджи', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Фьюжн', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Цезарь', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Эби тортилья', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Ямато', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Банзай', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Банкок', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Блэк', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Дуэт', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Калифорния c лососем', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Калифорния', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Калифорния микс', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Калифорния с креветкой', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Калифорния с угрем', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Камикадзе', bot.send_photo, 'photo')),

    loop.create_task(uploadPhoto('Канада', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Канада лайт', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Канада с креветкой', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Запад', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Икура маки', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Калифорния темпура', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Мадагаскар', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сафари', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сяки темпура', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сяки терияки', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сяки хот', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Токио', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Тэка хот', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Умэ', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Унаги хот', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Эби темпура', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Яки нику', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Якудза', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Краб', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Мидии', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сансей', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Суши-Пицца', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Филадельфия запеченная', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Чикен-Чуз', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Яки-Магура', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Яки-Фурай', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Яки-Хокайдо', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Икура', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Кани', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Лосось терияки', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Макеши', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Микадо', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Огурец', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Такуан', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Тори', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Тэка', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Умаджи', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Чука', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Эби', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Ясай', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Панда', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Радуга', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сэйджи', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Шеф Ролл', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Осака', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Картофель Фри', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Креветки Темпура', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Наггетсы(6шт)', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Наггетсы(10шт)', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Кальмар', bot.send_photo, 'photo')),

    loop.create_task(uploadPhoto('Креветка', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Лосось', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Икура', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Спайси', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сырный', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Удон с говядиной', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Удон с креветкой', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Удон с курицей', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Удон с лососем', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Удон с овощами', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Удон с угрем', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Удон со свининой', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Бургер 1', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Бургер 2', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Бургер 3', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Бургер 4', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Бургер 5', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Запеченный Сет', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 1', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 2', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 3', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 4', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 5', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 6', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 7', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 8', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет 9', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет DOS', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет Ассорти', bot.send_photo, 'photo')),
    loop.create_task(uploadPhoto('Сет Праздничный', bot.send_photo, 'photo')),
]'''


