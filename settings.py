import os
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()

# подключаемся к MySQL Workbench
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_READ_HOST'),
    'user': os.getenv('MYSQL_READ_USER'),
    'password': os.getenv('MYSQL_READ_PASSWORD'),
    'database': os.getenv('MYSQL_READ_DB'),
    'port': int(os.getenv('MYSQL_READ_PORT', 3306)),  # Добавляем порт, с дефолтом 3306
    'cursorclass': DictCursor
}

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_AUTH_DB = os.getenv('MONGO_AUTH_DB')
MONGO_COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME')

# подключаемся к MongoDB
MONGO_CONFIG = (f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}'
             f'@{MONGO_HOST}/?readPreference=primary&ssl=false'
             f'&authMechanism=DEFAULT&authSource={MONGO_AUTH_DB}')