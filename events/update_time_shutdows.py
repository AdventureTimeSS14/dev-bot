import time
from datetime import timedelta

import discord
from discord.ext import tasks

from bot_init import bot


@tasks.loop(seconds=11)
async def update_time_shutdows():
    """
    Задача, которая будет обновлять статус редактируя сообщение.
    """

    channel_id = 1320771026019422329  # ID канала, где нужно редактировать сообщение
    message_id = 1320771150938243195  # ID сообщения, которое нужно редактировать

    # Получаем канал
    channel = bot.get_channel(channel_id)
    if channel is None:
        print(f"Не удалось найти канал с ID {channel_id}")
        return  # Если канал не найден, прекращаем выполнение

    try:
        # Получаем сообщение по ID
        message = await channel.fetch_message(message_id)
        
        if not hasattr(bot, 'start_time') or bot.start_time is None:
            await message.edit(content=f"Время не задано.")
            return  # Если время старта не задано, пропускаем обновление

        # Вычисляем прошедшее время с момента старта
        elapsed_time = time.time() - bot.start_time
        elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))

        # Оставшееся время до отключения
        remaining_time = (5 * 3600 + 57 * 60) - elapsed_time
        remaining_time_str = str(timedelta(seconds=int(remaining_time)))

        # Редактируем отправленное сообщение
        await message.edit(content=f"Время работы бота: {elapsed_time_str}\nОставшееся время до отключения: {remaining_time_str}")

    except discord.NotFound:
        print(f"Сообщение с ID {message_id} не найдено.")
    except discord.Forbidden:
        print("У бота нет прав для редактирования сообщения.")
    except Exception as e:
        print(f"Произошла ошибка при редактировании сообщения: {e}")