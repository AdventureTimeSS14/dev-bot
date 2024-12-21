import sys
import requests
from config import AUTHOR, GITHUB

OWNER = AUTHOR
REPO = 'Dev-bot'
API_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/runs'

# Заголовки для аутентификации
headers = {
    'Authorization': f'token {GITHUB}',
    'Accept': 'application/vnd.github.v3+json',
}

# Функция для получения состояния всех запущенных workflow
def check_workflows():
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()

        workflows = response.json()

        # Проверяем все workflow
        for run in workflows['workflow_runs']:
            run_name = run['name']
            status = run['status']
            conclusion = run['conclusion']
            created_at = run['created_at']

            # Если хотя бы один процесс в статусе 'in_progress', завершаем программу
            if status == 'in_progress':
                print(f"  - {run_name}")
                print(f"    Статус: {status}")
                print(f"    Результат: {conclusion if conclusion else 'Не завершено'}")
                print(f"    Дата начала: {created_at}")
                print()
            
                print(f"Есть запущенные workflow (статус 'in_progress'). Завершаем процесс...")
                sys.exit(0)

        # Если все процессы завершены, программа продолжит выполнение
        print("Нет запущенных workflow в статусе 'in_progress'. Продолжаем работу.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к GitHub API: {e}")
        sys.exit(1)