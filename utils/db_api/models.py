
from sqlalchemy import sql, Sequence, Column, Integer, String, TIMESTAMP, JSON, Boolean, BigInteger

from utils.db_api.database import db



# Создаем класс таблицы товаров
class Item(db.Model):
    __tablename__ = 'items'
    query: sql.Select

    # Уникальный индификатор товара
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    # Код категории (для отображения в колбек дате)
    category_code = Column(String(20))

    # Код подкатегории (для отображения в колбек дате)
    subcategory_code = Column(String(20))

    # Название категории (для отображения в кнопке)
    category_name = Column(String(50))

    # Название подкатегории (для отображения на кнопке)
    subcategory_name = Column(String(50))


    # Название, фото и цена товара
    name = Column(String(50))
    price = Column(Integer)
    description = Column(String(350))
    weight = Column(Integer)

    def __repr__(self):
        return f"""
Товар: {self.id} - "{self.name}"
Цена: {self.price}
"""

class PurchaseItem(db.Model):
    __tablename__ = 'purchase'
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    buyer = Column(BigInteger)
    item_name = Column(String(255))
    receiver = Column(String(100))
    purchase_time = Column(TIMESTAMP)
    amount = Column(Integer)
    shipping_address = Column(String(250))
    phone_number = Column(String(50))
    delivery_method = Column(String(50))

class Photo(db.Model):
    __tablename__ = 'photo'
    query: sql.Select

    id = Column(Integer, primary_key=True)
    file_id = Column(String(255))
    filename = Column(String(255))
    product = Column(String(255))

class ShoppingCart(db.Model):
    __tablename__='ShoppingCart'
    query: sql.Select

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    item_id = Column(Integer)
    item_name = Column(String(255))
    quantity = Column(Integer)
    amount = Column(Integer)







