import re

import requests
from fuzzywuzzy import fuzz

from bot_init import bot
from config import AUTHOR, GLOBAL_SESSION, REPOSITORIES
from data import JsonData


@bot.event
async def on_message(message):
    """
    Обработчик сообщений бота.
    """
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return

    # Обработка команд
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    # Ответ на упоминание бота
    if f"<@{bot.user.id}>" in message.content:
        await handle_mention(message)
        return

    # Проверка шаблона GitHub issue/PR
    await handle_github_pattern(message)


async def handle_mention(message):
    """
    Обрабатывает упоминания бота и отвечает на определённые фразы.
    """
    text_without_mention = message.content.replace(f"<@{bot.user.id}>", "").strip()
    data = JsonData()
    
    # Проверяем вариации фраз из JsonData
    for variation in data.get_data('hug_variations'):
        if fuzz.token_sort_ratio(text_without_mention.lower(), variation) > 80:
            await message.channel.send("*Обнимает в ответ.*")
            break


async def handle_github_pattern(message):
    """
    Проверяет наличие шаблона GitHub issue/PR в сообщении и отправляет ссылку на него.
    """
    match = re.search(r'\[(n|o)(\d+)\]', message.content)
    if match:
        repo_code, number = match.groups()
        link = check_github_issue_or_pr(repo_code, number)
        if link:
            await message.channel.send(link)


def check_github_issue_or_pr(repo_code, number):
    """
    Проверяет, существует ли GitHub issue или PR с указанным номером, и возвращает ссылку.
    """
    repo_name = REPOSITORIES.get(repo_code)
    if not repo_name:
        print(f"⚠️ Репозиторий с кодом {repo_code} не найден.")
        return None

    base_api_url = f'https://api.github.com/repos/{AUTHOR}/{repo_name}'
    issue_url = f'{base_api_url}/issues/{number}'
    pr_url = f'{base_api_url}/pulls/{number}'

    try:
        # Проверка PR
        pr_response = GLOBAL_SESSION.get(pr_url)
        if pr_response.status_code == 200:
            pr_data = pr_response.json()
            return f"[{repo_name} PR {number}]({pr_data['html_url']})"

        # Проверка Issue
        issue_response = GLOBAL_SESSION.get(issue_url)
        if issue_response.status_code == 200:
            issue_data = issue_response.json()
            return f"[{repo_name} Issue {number}]({issue_data['html_url']})"

    except requests.RequestException as e:
        print(f"❌ Ошибка при запросе к GitHub API: {e}")

    return None
