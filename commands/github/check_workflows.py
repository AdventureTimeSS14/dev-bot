import sys

import aiohttp

from bot_init import bot
from commands.misc.shutdows_deff import shutdown_def
from config import AUTHOR, GITHUB

OWNER = AUTHOR
REPO = 'Dev-bot'
API_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/runs'

# Заголовки для аутентификации
HEADERS = {
    'Authorization': f'token {GITHUB}',
    'Accept': 'application/vnd.github.v3+json',
}

async def check_workflows():
    """
    Проверяет состояние запущенных GitHub Actions workflows и завершает работу бота,
    если обнаружено более одного процесса с состоянием 'in_progress' для workflow с именем 'Deploy Discord-Bot'.
    """
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(API_URL) as response:
                if response.status != 200:
                    print(f"❌ Ошибка при подключении к GitHub API. Статус: {response.status}")
                    sys.exit(1)

                workflows = await response.json()

        in_progress_count = 0  # Количество процессов со статусом 'in_progress'

        # Проверяем все workflows
        for run in workflows.get('workflow_runs', []):
            run_name = run.get('name', 'Неизвестно')
            
            # Проверяем, что имя процесса соответствует 'Deploy Discord-Bot'
            if run_name == 'Deploy Discord-Bot':
                in_progress_count += 1

            status = run.get('status', 'Неизвестно')
            conclusion = run.get('conclusion', 'Не завершено')
            created_at = run.get('created_at', 'Неизвестно')

            # Увеличиваем счетчик, если процесс в статусе 'in_progress'
            if status == 'in_progress':
                

                # Логируем информацию о процессе
                print(f"  - Название: {run_name}")
                print(f"    Статус: {status}")
                print(f"    Результат: {conclusion}")
                print(f"    Дата начала: {created_at}")
                print()

                # Если больше одного процесса в статусе 'in_progress', завершаем работу
                if in_progress_count > 1:
                    print("❌ Обнаружено более одного запущенного workflow 'Deploy Discord-Bot'. Завершаем процесс...")
                    await bot.close()
                    sys.exit(0)

        # Логируем результат проверки
        if in_progress_count == 0:
            print("✅ Нет запущенных workflow 'Deploy Discord-Bot' в статусе 'in_progress'. Продолжаем работу.")
        else:
            print(f"⚠️ Обнаружено {in_progress_count} запущенный(ых) workflow 'Deploy Discord-Bot' в статусе 'in_progress'. Продолжаем работу.")

    except aiohttp.ClientError as e:
        print(f"❌ Ошибка при подключении к GitHub API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")
        sys.exit(1)
