import asyncio
import os
import sys

import discord

from bot_init import bot
from commands.misc.shutdows_deff import shutdown_def
from config import LOG_CHANNEL_ID, TIME_SHUTDOWSE


async def shutdown_after_time():
    await asyncio.sleep(TIME_SHUTDOWSE)  # 5 часов и 57 минут в секундах
    print(f"Время истекло. Завершаем работу {bot.user}.")
    
    channel = bot.get_channel(LOG_CHANNEL_ID)
    # await channel.send(f"{bot.user} завершает свою работу! Ожидайте перезапуска в течении 10 минут.")
    await shutdown_def()
    
    # # Получаем путь к файлу в папке выше
    # log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bot_logs.log')
    # # Отправляем лог-файл
    # with open(log_file_path, "rb") as log_file:
    #     await channel.send("Бот завершает свою работу. Вот лог-файл:", file=discord.File(log_file, "bot_logs.log"))
        
    await bot.close()  # Завершаем работу бота
    sys.exit(0)