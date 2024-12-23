import asyncio
import signal

from bot_init import bot
from commands import (echo_command, gpt_command, help_command,
                      list_team_command, ping_command, restart_command,
                      uptime_command, user_role_command)
from commands.adt_team import (add_role_command, add_vacation_command,
                               end_vacation_command, new_team_command,
                               remove_role_command, remove_team_command,
                               team_help_command, tweak_team_command)
from commands.dbCommand import help_command, info_command, status_command
from commands.github import (achang_command, check_workflows, forks_command,
                             github_processor, milestones_command,
                             pr_changelog_send, review_command)
from commands.misc.shutdows_deff import shutdown_def
from config import DISCORD_KEY
from events import on_command, on_error, on_message, on_ready, update_status


# Функция для обработки сигнала SIGTERM
async def handle_sigterm():
    print("Получен сигнал SIGTERM. Отключение бота...")
    await shutdown_def()
    # Завершаем работу бота
    asyncio.create_task(bot.close())

# Функция для обработки SIGINT (Ctrl+C или завершение через терминал)
async def handle_sigint():
    print("Получен сигнал SIGINT. Отключение бота...")
    await shutdown_def()
    # Завершаем работу бота
    asyncio.create_task(bot.close())

# Устанавливаем обработчики сигналов
signal.signal(signal.SIGTERM, lambda *args: handle_sigterm())
signal.signal(signal.SIGINT, lambda *args: handle_sigint())


if __name__ == '__main__':
    bot.run(DISCORD_KEY)

#TODO: Add logging: @nixsilvam404
# Настройка логирования, сохраняем логи в файл
# Настройка глобального логирования
# logging.basicConfig(
#     level=logging.DEBUG,  # Логируем все сообщения с уровня DEBUG и выше
#     format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
#     handlers=[
#         logging.FileHandler("bot_logs.log"),  # Записываем логи в файл bot_logs.log
#         logging.StreamHandler(sys.stdout)     # Также выводим логи в консоль
#     ]
# )