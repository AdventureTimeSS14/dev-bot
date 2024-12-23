import time

from bot_init import bot
from commands.github import check_workflows
from commands.github.git_fetch_pull import fetch_merged_pull_requests
from commands.list_team_command import list_team_task
from config import LOG_CHANNEL_ID
from events.check_new_commit import monitor_commits
from events.shutdows_after_time import shutdown_after_time
from events.update_status import (update_status,
                                  update_status_server_message_eddit)
from events.update_time_shutdows import update_time_shutdows


async def start_task_if_not_running(task, task_name: str):
    """
    Запускает задачу, если она еще не запущена.
    """
    if not task.is_running():
        task.start()
        print(f"✅ Задача {task_name} запущена.")
    else:
        print(f"⚙️ Задача {task_name} уже работает.")


@bot.event
async def on_ready():
    """
    Событие, которое выполняется при запуске бота.
    """
    bot.start_time = time.time()  # Сохраняем время старта бота

    # Проверка workflows на случай повторного запуска на GitHub Actions
    await check_workflows.check_workflows()  # Завершает работу, если бот уже запущен на GitHub Actions

    # Запуск всех фоновых задач
    await start_task_if_not_running(fetch_merged_pull_requests, "fetch_merged_pull_requests")
    await start_task_if_not_running(list_team_task, "list_team_task")
    await start_task_if_not_running(monitor_commits, "monitor_commits")
    await start_task_if_not_running(update_status, "update_status")
    await start_task_if_not_running(update_status_server_message_eddit, "update_status_server_message_eddit")
    await start_task_if_not_running(update_time_shutdows, "update_time_shutdows")

    print(f"Bot {bot.user} is ready to work!")  # Лог в консоль

    # Уведомляем в лог-канале, что бот активен
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f"{bot.user} активен!")
    else:
        print(f"❌ Не удалось найти канал с ID {LOG_CHANNEL_ID} для логов.")

    # Запуск задачи для автоматического завершения работы через определённое время
    bot.loop.create_task(shutdown_after_time())
