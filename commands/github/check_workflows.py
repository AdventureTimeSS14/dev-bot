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
        response.raise_for_status()  # Проверяем на ошибки HTTP

        workflows = response.json()

        # Если запущены workflow, то завершить процесс
        if workflows['total_count'] > 0:
            print("Есть запущенные workflow. Завершаем процесс...")
            sys.exit(0)
        else:
            print("Нет запущенных workflow. Продолжаем работу.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к GitHub API: {e}")
        sys.exit(1)