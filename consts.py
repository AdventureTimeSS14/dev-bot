import os

from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем значение DISCORD_KEY из .env
DISCORD_KEY = os.getenv('DISCORD_KEY')

# Проверяем, установлено ли значение
if not DISCORD_KEY:
  raise ValueError("DISCORD_KEY не найден в файле .env")