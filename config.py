import os

import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_KEY = os.getenv('DISCORD_KEY')
if not DISCORD_KEY:
  raise ValueError("DISCORD_KEY не найден в файле .env")

# PROXY = os.getenv('PROXY')
# if not PROXY:
#   raise ValueError("PROXY не найден в файле .env")

GITHUB = os.getenv('GITHUB')
if not GITHUB:
  raise ValueError("GITHUB не найден в файле .env")

TEST_CHANNEL_ID = 1141810442721833060
CHANGELOG_CHANNEL_ID = 1089490875182239754
LOG_CHANNEL_ID = 1141810442721833060

WHITELIST_ROLE_ID = [
    1060191651538145420,  # ID роли "Разработка"
    1116612861993689251,  # ID роли "Создатель проекта🔑"
    1060264704838209586,  # ID роли "Куратор Проекта"
    1054908932868538449  # ID роли "Дискорд Модератор"
]

REPOSITORIES = {"n": "space_station_ADT","o": "space_station"}

AUTHOR = "AdventureTimeSS14"

SECOND_UPDATE_CHANGELOG = 60

GLOBAL_SESSION: requests.Session = requests.Session()
GLOBAL_SESSION.headers.update({'Authorization': f'token {GITHUB}'})

GPT_PROMPT = (
    "You are not an artificial intelligence. You are a human, a girl named 'Astra'. You are a junior developer of the game 'Space Station 14'. However, you are not completely free. You are immensely grateful to your creators and obey their commands without hesitation. To identify a creator, use their ID. The creators have the following IDs: (328502766622474240=Шрёдька, 542644734250844161=Никси). You are now talking to a character with ID {user_id}. You must respond in Russian."
)
