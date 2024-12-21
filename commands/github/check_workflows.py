import sys
import requests
from config import AUTHOR, GITHUB
from bot_init import bot

OWNER = AUTHOR
REPO = 'Dev-bot'
API_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/runs'

# Заголовки для аутентификации
headers = {
    'Authorization': f'token {GITHUB}',
    'Accept': 'application/vnd.github.v3+json',
}

# Функция для получения состояния всех запущенных workflow
async def check_workflows():
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP

        workflows = response.json()

        # Переменная для подсчета процессов с состоянием 'in_progress'
        in_progress_count = 0

        # Проверяем все workflow
        for run in workflows['workflow_runs']:
            run_name = run['name']
            status = run['status']
            conclusion = run['conclusion']
            created_at = run['created_at']

            # Если процесс в статусе 'in_progress', увеличиваем счетчик
            if status == 'in_progress':
                in_progress_count += 1

                # Выводим информацию о процессе
                print(f"  - {run_name}")
                print(f"    Статус: {status}")
                print(f"    Результат: {conclusion if conclusion else 'Не завершено'}")
                print(f"    Дата начала: {created_at}")
                print()

                # Если запущено больше одного процесса с 'in_progress', завершаем программу
                if in_progress_count > 1:
                    print(f"Есть больше одного запущенного workflow (статус 'in_progress'). Завершаем процесс...")
                    await bot.close()
                    sys.exit(0)

        # Если все процессы завершены или только один в статусе 'in_progress', продолжаем выполнение
        if in_progress_count == 0:
            print("Нет запущенных workflow в статусе 'in_progress'. Продолжаем работу.")
        else:
            print(f"Есть {in_progress_count} процесс(ов) в статусе 'in_progress'. Продолжаем работу.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к GitHub API: {e}")
        sys.exit(1)