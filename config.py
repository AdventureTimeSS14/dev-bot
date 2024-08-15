import os

from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем значение DISCORD_KEY из .env
DISCORD_KEY = os.getenv('DISCORD_KEY')
PROXY = os.getenv('PROXY')
GITHUB = os.getenv('GITHUB')

whitelist_role = [
    1060191651538145420,  # ID роли "Разработка"
    1116612861993689251,  # ID роли "Создатель проекта🔑"
    1060264704838209586,  # ID роли "Куратор Проекта"
    1054908932868538449  # ID роли "Дискорд Модератор"
]
author = "AdventureTimeSS14"

# Проверяем, установлено ли значение
if not DISCORD_KEY:
  raise ValueError("DISCORD_KEY не найден в файле .env")

if not PROXY:
  raise ValueError("PROXY не найден в файле .env")

if not GITHUB:
  raise ValueError("GITHUB не найден в файле.env")