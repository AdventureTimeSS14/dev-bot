import time
from datetime import timedelta
from discord.ext import tasks
from bot_init import bot

@tasks.loop(seconds=2)  # Обновляем статус каждую 2 секунды
async def update_time_shutdows(initial_message):
    """
    Задача, которая будет обновлять статус каждую секунду или две.
    """
    initial_message = 1320771150938243195 # Сообщение которое будет редактировать
    
    if not hasattr(bot, 'start_time') or bot.start_time is None:
        await initial_message.edit(content=f"Время не задано.")
        return  # Если время старта не задано, пропускаем обновление

    # Вычисляем прошедшее время с момента старта
    elapsed_time = time.time() - bot.start_time
    elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))

    # Оставшееся время до отключения
    remaining_time = (5 * 3600 + 57 * 60) - elapsed_time
    remaining_time_str = str(timedelta(seconds=int(remaining_time)))

    # Редактируем отправленное сообщение
    await initial_message.edit(content=f"Время работы бота: {elapsed_time_str}\nОставшееся время до отключения: {remaining_time_str}")
