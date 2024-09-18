from bot_init import bot
from config import LOG_CHANNEL_ID
import asyncio

@bot.event
async def on_error(event, *args, **kwargs):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(f"Произошла ошибка: {event}")