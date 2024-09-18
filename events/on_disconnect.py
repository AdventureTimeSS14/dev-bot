from bot_init import bot
from config import LOG_CHANNEL_ID
import asyncio

@bot.event
async def on_disconnect():
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(f"{bot.user} отключена!")


