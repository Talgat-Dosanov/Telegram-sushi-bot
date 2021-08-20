from typing import List

from sqlalchemy import and_

from utils.db_api.models import Item, Photo, ShoppingCart, PurchaseItem
from utils.db_api.database import db


# Функция для создания нового товара в базе данных. Принимает все возможные аргументы, прописанные в Item
#async def add_item(**kwargs):
   # new_item = await Item(**kwargs).create()
   # return new_item


# Функция для вывода товаров с РАЗНЫМИ категориями
async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_name).gino.all()


# Функция для вывода товаров с РАЗНЫМИ подкатегориями в выбранной категории
async def get_subcategories(category) -> List[Item]:
    return await Item.query.distinct(Item.subcategory_name).where(Item.category_code == category).gino.all()


# Функция для подсчета товаров с выбранными категориями и подкатегориями
async def count_items(category_code, subcategory_code=None):
    # Прописываем условия для вывода (категория товара равняется выбранной категории)
    conditions = [Item.category_code == category_code]

    # Если передали подкатегорию, то добавляем ее в условие
    if subcategory_code:
        conditions.append(Item.subcategory_code == subcategory_code)

    # Функция подсчета товаров с указанными условиями
    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total


# Функция вывода всех товаров, которые есть в переданных категориях
async def get_items(category_code) -> List[Item]:
    item = await Item.query.distinct(Item.name).where(Item.category_code == category_code).gino.all()
    return item

# Функция вывода всех товаров, которые есть в переданных категории и подкатегории
async def get_items_with_subcategory(category_code, subcategory_code) -> List[Item]:
    item = await Item.query.distinct(Item.name).where(and_(Item.category_code == category_code,
                                                           Item.subcategory_code == subcategory_code)).gino.all()
    return item
# Функция для получения объекта товара по его айди
async def get_item(item_id) -> Item:
     item = await Item.query.where(Item.id == item_id).gino.first()
     return item
# Получаем фото из базы данных
async def get_photo(product) -> Photo:
    photo = await Photo.query.distinct(Photo.file_id).where(Photo.product == product).gino.first()
    return photo

# Получаем добавленные в корзину товары по user_id
async def get_items_from_shipping_cart(user_id) -> List[ShoppingCart]:
    items = await ShoppingCart.query.where(ShoppingCart.user_id == user_id).gino.all()
    return items

# Очищаем корзину
async def delete_cart(user_id) -> List[ShoppingCart]:
    delete_items = await ShoppingCart.delete.where(ShoppingCart.user_id == user_id).gino.all()
    return delete_items

# Получаем заказ по id
async def get_order(order_id) -> PurchaseItem:
    order = await PurchaseItem.query.where(PurchaseItem.id == order_id).gino.first()
    return order

# Удалить товар из базы
async def delete_item(name) -> Item:
    item = await Item.delete.where(Item.name == name).gino.first()
    return item

# Удалить фото из базы
async def delete_photo(name) -> Photo:
    photo = await Photo.delete.where(Photo.product == name).gino.first()
    return photo

# Список всех уникальных пользователей из базы
async def get_id_users() -> List[PurchaseItem]:
    users = await PurchaseItem.query.distinct(PurchaseItem.buyer).gino.all()
    return users
# Функция получения всех имен товаров в базе
async def get_all_items() -> List[Item]:
    return await Item.query.distinct(Item.name).gino.all()

# Функция поиска подкатегории товара по имени товара
async def get_subcategory_name(category_name) -> Item:
    subcategory_code = await Item.query.distinct(Item.subcategory_code).where(
        Item.subcategory_name == category_name).gino.first()
    return subcategory_code

# Функция поиска товара по названию
async def find_item(item_name) -> Item:
    return await Item.query.distinct(Item.name).where(Item.name == item_name).gino.first()
