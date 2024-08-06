import os

from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем значение DISCORD_KEY из .env
DISCORD_KEY = os.getenv('DISCORD_KEY')
PROXY = os.getenv('PROXY')
GITHUB = os.getenv('GITHUB')

# Проверяем, установлено ли значение
if not DISCORD_KEY:
  raise ValueError("DISCORD_KEY не найден в файле .env")

if not PROXY:
  raise ValueError("PROXY не найден в файле .env")

if not GITHUB:
  raise ValueError("GITHUB не найден в файле.env")