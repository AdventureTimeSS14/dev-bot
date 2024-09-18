from bot_init import bot
from config import LOG_CHANNEL_ID
import asyncio
import datetime

@bot.event
async def on_command(ctx):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        # Получаем текущее время
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Формируем сообщение с дополнительной информацией
        log_message = (
            f"Команда выполнена: {ctx.command.name}\n"
            f"Пользователь: {ctx.author} (ID: {ctx.author.id})\n"
            f"Канал: {ctx.channel} (ID: {ctx.channel.id})\n"
            f"Время: {current_time}\n"
            f"Ссылка на сообщение: [Перейти к сообщению](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id})"
        )
        
        await channel.send(log_message)
    print(f"Команда выполнена: {ctx.command.name} от {ctx.author} в канале {ctx.channel} в {current_time}")