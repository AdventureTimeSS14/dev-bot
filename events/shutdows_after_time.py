import asyncio
import sys

from bot_init import bot
from commands.misc.shutdows_deff import shutdown_def
from config import TIME_SHUTDOWSE


async def shutdown_after_time():
    """
    Ожидает заданное время (в секундах) и затем инициирует завершение работы бота.
    """
    await asyncio.sleep(TIME_SHUTDOWSE)  # Ожидаем заданное время (например, 5 часов и 57 минут)

    print(f"Время истекло. Завершаем работу {bot.user}.")

    # Отправка сообщения в канал логов (пока закомментировано)
    # channel = bot.get_channel(LOG_CHANNEL_ID)
    # await channel.send(f"{bot.user} завершает свою работу!
    # Ожидайте перезапуска в течение 10 минут.")

    # Завершаем работу с использованием команды shutdown
    await shutdown_def()

    # Закрытие работы бота
    await bot.close()
    sys.exit(0)
