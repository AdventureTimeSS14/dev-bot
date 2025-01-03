import logging
import time
import asyncio

from bot_init import bot
from commands.github import check_workflows
from config import LOG_CHANNEL_ID
from events.shutdows_after_time import shutdown_after_time
from tasks.check_new_commit_task import monitor_commits
from tasks.git_fetch_pull_task import fetch_merged_pull_requests
from tasks.list_team_task import list_team_task
from tasks.update_status_presence_task import update_status_presence
from tasks.update_status_server_message_eddit_task import (
    update_status_server_message_eddit,
)
from tasks.update_time_shutdows_task import update_time_shutdows


async def start_task_if_not_running(task, task_name: str):
    """
    Запускает задачу, если она еще не запущена.
    """
    if not task.is_running():
        asyncio.create_task(task())  # Используем asyncio.create_task
        print(f"✅ Задача {task_name} запущена.")
    else:
        print(f"⚙️ Задача {task_name} уже работает.")


@bot.event
async def on_ready():
    """
    Событие, которое выполняется при запуске бота.
    """
    logging.info(
        "Bot %s (ID: %d) is ready to work!", bot.user.name, bot.user.id
    )
    logging.info("Connected to Discord successfully.")
    guild_names = [guild.name for guild in bot.guilds]
    logging.info("Guilds: %s", guild_names)  # Выводит список серверов, к которым подключен бот.

    print("✅ Connected to Discord successfully.")
    print(f"✅ Guilds: {guild_names}")  # Выводит список серверов, к которым подключен бот.

    bot.start_time = time.time()  # Сохраняем время старта бота

    # Проверка workflows на случай повторного запуска на GitHub Actions
    await check_workflows.check_workflows()  # Завершает работу,
                                             # если бот уже запущен на GitHub Actions

    # Запуск всех фоновых задач
    await start_task_if_not_running(
        fetch_merged_pull_requests, "fetch_merged_pull_requests"
    )
    await start_task_if_not_running(list_team_task, "list_team_task")
    await start_task_if_not_running(monitor_commits, "monitor_commits")
    await start_task_if_not_running(
        update_status_presence, "update_status_presence"
    )
    await start_task_if_not_running(
        update_status_server_message_eddit, "update_status_server_message_eddit"
    )
    await start_task_if_not_running(
        update_time_shutdows, "update_time_shutdows"
    )

    print(f"✅ Bot {bot.user.name} (ID: {bot.user.id}) is ready to work!")

    # Уведомляем в лог-канале, что бот активен
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(
            content=(
                f"✅ **{bot.user.name} успешно активирована!**\n"
                f"🔹 **Статус:** Бот запущен и готов к работе.\n_ _"
            )
        )
    else:
        print(f"❌ Не удалось найти канал с ID {LOG_CHANNEL_ID} для логов.")

    # Запуск задачи для автоматического завершения работы через определённое время
    asyncio.create_task(shutdown_after_time())  # Используем asyncio.create_task
