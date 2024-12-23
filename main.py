import asyncio
import signal
import sys
import logging

from config import DISCORD_KEY
from commands.misc.shutdows_deff import shutdown_def  # Для выполнения завершающих операций




from bot_init import bot
from commands import (echo_command, gpt_command, help_command, ping_command,
                      restart_command, status_command, uptime_command,
                      user_role_command)
from commands.adt_team import (add_role_command, add_vacation_command,
                               end_vacation_command, new_team_command,
                               remove_role_command, remove_team_command,
                               team_help_command, tweak_team_command)
from commands.dbCommand import help_command, info_command, status_command
from commands.github import (achang_command, check_workflows, forks_command,
                             github_processor, milestones_command,
                             pr_changelog_send, review_command)
from events import on_command, on_error, on_message, on_ready, update_status


# Настраиваем глобальное логирование
logging.basicConfig(
    level=logging.INFO,  # Устанавливаем уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot_logs.log"),  # Сохраняем логи в файл
        logging.StreamHandler(sys.stdout),  # Отображаем логи в консоли
    ],
)


async def shutdown(signal_type=None):
    """
    Завершение работы бота при получении сигнала или исключении.
    """
    logging.info(f"Получен сигнал: {signal_type.name if signal_type else 'Manual Exit'}. Завершаем работу...")
    try:
        await shutdown_def()  # Выполняем пользовательские действия перед завершением работы
        await bot.close()  # Закрываем соединение бота
    except Exception as e:
        logging.error(f"Ошибка при завершении работы бота: {e}")
    finally:
        sys.exit(0)  # Принудительно завершаем процесс


def setup_signal_handlers():
    """
    Настройка обработчиков сигналов для корректного завершения работы.
    """
    if sys.platform == "win32":
        # Windows не поддерживает сигналы SIGINT/SIGTERM для asyncio
        logging.warning("Сигналы SIGINT и SIGTERM не поддерживаются на Windows.")
    else:
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(s)))


async def main():
    """
    Основная функция запуска бота.
    """
    try:
        setup_signal_handlers()  # Настраиваем обработчики сигналов
        logging.info("Запуск бота...")
        await bot.start(DISCORD_KEY)  # Запускаем бота с токеном
    except (KeyboardInterrupt, SystemExit):
        await shutdown()  # Обрабатываем принудительное завершение
    except Exception as e:
        logging.error(f"Неожиданная ошибка при запуске бота: {e}")
        await shutdown()


if __name__ == "__main__":
    bot.run(DISCORD_KEY)
