import time

from bot_init import bot
from commands.github import check_workflows
from commands.github.git_fetch_pull import fetch_merged_pull_requests
from commands.list_team_command import list_team_task
from config import LOG_CHANNEL_ID
from events.check_new_commit import monitor_commits
from events.shutdows_after_time import shutdown_after_time
from events.update_status import update_status
from events.update_time_shutdows import update_time_shutdows


@bot.event
async def on_ready():
    bot.start_time = time.time()  # Сохраняем время старта бота в атрибуте объекта bot

    await check_workflows.check_workflows() # Завершаем работу, если уже бот запущен на GitGub Action
    
    if not fetch_merged_pull_requests.is_running():
        fetch_merged_pull_requests.start()
        
    if not list_team_task.is_running():
        list_team_task.start()
        
    if not monitor_commits.is_running():
        monitor_commits.start()
        
    if not update_status.is_running():
        update_status.start()
        
    if not update_time_shutdows.is_running():
        update_time_shutdows.start()
        
    print(f"Bot {bot.user} is ready to work!")
    
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(f"{bot.user} активна!")

    bot.loop.create_task(shutdown_after_time()) # Запуск задачи для завершения работы через 5 часов 57 минут