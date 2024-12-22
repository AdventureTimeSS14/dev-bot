import asyncio
import os
import sys

import discord

from bot_init import bot
from config import LOG_CHANNEL_ID


async def shutdown_after_time():
    await asyncio.sleep(5 * 3600 + 57 * 60)  # 5 часов и 57 минут в секундах
    print(f"Время истекло. Завершаем работу {bot.user}.")
    
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(f"{bot.user} завершает свою работу! Ожидайте перезапуска в течении 10 минут.")
    
    # # Получаем путь к файлу в папке выше
    # log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bot_logs.log')
    # # Отправляем лог-файл
    # with open(log_file_path, "rb") as log_file:
    #     await channel.send("Бот завершает свою работу. Вот лог-файл:", file=discord.File(log_file, "bot_logs.log"))
        
    await bot.close()  # Завершаем работу бота
    sys.exit(0)