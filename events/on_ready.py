from bot_init import bot
from commands.github.git_fetch_pull import fetch_merged_pull_requests


@bot.event
async def on_ready():
    if not fetch_merged_pull_requests.is_running():
        fetch_merged_pull_requests.start()
    print(f"Bot {bot.user} is ready to work!")