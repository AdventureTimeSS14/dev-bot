# commands/uptime_command.py
import time
from datetime import timedelta

from bot_init import bot


@bot.command()
async def uptime(ctx):
    if not hasattr(bot, 'start_time') or bot.start_time is None:
        await ctx.send("Бот еще не запущен.")
        return

    # Вычисляем прошедшее время с момента старта
    elapsed_time = time.time() - bot.start_time
    elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))

    # Оставшееся время до отключения
    remaining_time = (5 * 3600 + 57 * 60) - elapsed_time
    remaining_time_str = str(timedelta(seconds=int(remaining_time)))

    await ctx.send(f"Время работы бота: {elapsed_time_str}\nОставшееся время до отключения: {remaining_time_str}")
