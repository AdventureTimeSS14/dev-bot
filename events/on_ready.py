import asyncio

from bot_init import bot
from commands.github import check_workflows
from commands.github.git_fetch_pull import fetch_merged_pull_requests
from commands.list_team_command import list_team_task
from config import LOG_CHANNEL_ID


@bot.event
async def on_ready():
    if not fetch_merged_pull_requests.is_running():
        fetch_merged_pull_requests.start()
    if not list_team_task.is_running():
        list_team_task.start()
    print(f"Bot {bot.user} is ready to work!")
    channel = bot.get_channel(LOG_CHANNEL_ID)
    check_workflows.check_workflows() # Завершаем работу, если уже бот запущен на GitGub Action
    await channel.send(f"{bot.user} активна!")
