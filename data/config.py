from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Забираем значение типа str
ADMINS = [
    os.getenv("ADMIN_ID"),
]  # Тут у нас будет список из админов
IP = os.getenv("ip")  # Тоже str, но для айпи адреса хоста


PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

# Ссылка на подключение к базе-данных
POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{DATABASE}'
aiogram_redis = {
    'host': IP
}
LP_TOKEN = os.getenv('LP_TOKEN')
redis = {
    'address': (IP,6379),
    'encoding': 'utf8'
}