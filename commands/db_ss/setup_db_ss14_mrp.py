from config import (
    DB_HOST,
    DB_DATABASE,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)

# Параметры подключения к базе данных
DB_PARAMS = {
    'database': DB_DATABASE,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}