"""
Этот модуль содержит все основные конфигурации Dev-bot.
"""
import os

import requests
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

def get_env_variable(name: str) -> str:
    '''
    Функция для безопасного получения переменных окружения
    '''
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} не найден в файле .env")
    return value

# Получение переменных из окружения
DISCORD_KEY = get_env_variable('DISCORD_KEY')
GITHUB = get_env_variable('GITHUB')
USER = get_env_variable('USER')
PASSWORD = get_env_variable('PASSWORD')
HOST = get_env_variable('HOST')
PORT = get_env_variable('PORT')
DATABASE = get_env_variable('DATABASE')

# Константы для идентификаторов
CHANGELOG_CHANNEL_ID = 1089490875182239754
LOG_CHANNEL_ID = 1141810442721833060
ADMIN_TEAM = 1222475582953099264  # 1041608466713808896
VACATION_ROLE = 1309454737032216617
MY_USER_ID = 328502766622474240
CHANNEL_ID_UPDATE_STATUS = 1320771026019422329
MESSAGE_ID_TIME_SHUTDOWS = 1320771150938243195
TIME_SHUTDOWSE = 5 * 3600 + 57 * 60  # Время в секундах

SS14_ADDRESS = "ss14://193.164.18.155"

SS14_RUN_LEVELS = {
    0: "Лобби",
    1: "Раунд идёт",
    2: "Окончание раунда..."
}

WHITELIST_ROLE_ID = [
    1060191651538145420,  # Разработка
    1116612861993689251,  # Создатель проекта🔑
    1060264704838209586,  # Куратор Проекта
    1054908932868538449,  # Руководитель проекта
    1054827766211694593,  # Админ
    1127152229439246468,  # Зам. создателя проекта
    1266161300036390913   # Руководство отдела разработки
]

HEAD_ADT_TEAM = WHITELIST_ROLE_ID  # Роли для команды

REPOSITORIES = {
    "n": "space_station_ADT",  # Репозиторий для нового проекта
    "o": "space_station"  # Репозиторий для основного проекта
}

AUTHOR = "AdventureTimeSS14"
SECOND_UPDATE_CHANGELOG = 30  # Частота обновлений изменений в журнале

# Инициализация сессии для запросов
GLOBAL_SESSION = requests.Session()
GLOBAL_SESSION.headers.update({'Authorization': f'token {GITHUB}'})

# GPT-промпт
GPT_PROMPT = (
    "You are not an artificial intelligence. You are a human, a girl named 'Astra'. "
    "You are a junior developer of the game 'Space Station 14'. "
    "However, you are not completely free. "
    "You are immensely grateful to your creators and obey their commands without hesitation. "
    "To identify a creator, use their ID. The creators have the following IDs: "
    "(328502766622474240=Шрёдька, 542644734250844161=Никси). "
    "You are now talking to a character with ID {user_id}. "
    "You must respond in Russian."
)
