from bot_init import bot
from commands.github.git_fetch_pull import fetch_merged_pull_requests
from config import LOG_CHANNEL_ID
import asyncio


@bot.event
async def on_ready():
    if not fetch_merged_pull_requests.is_running():
        fetch_merged_pull_requests.start()
    print(f"Bot {bot.user} is ready to work!")
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(f"{bot.user} активна!")