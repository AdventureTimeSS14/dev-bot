import re

import disnake
import requests
from fuzzywuzzy import fuzz

from bot_init import bot
from config import (
    ADMIN_TEAM,
    AUTHOR,
    GLOBAL_SESSION,
    LOG_CHANNEL_ID,
    REPOSITORIES,
    ADDRESS_MRP,
    POST_ADMIN_HEADERS,
)
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

    # Проверка сообщений в канале для удаления
    if message.channel.id == ADMIN_TEAM:
        await handle_message_deletion(message)

    if message.channel.id == 1309262152586235964:
        await send_ahat_message_post(message)

    # Проверка на шаблон GitHub issue/PR
    await handle_github_pattern(message)


async def handle_message_deletion(message):
    """
    Обрабатывает удаление сообщений в определенном канале и логирует информацию.
    """
    await message.delete()

    user = message.author
    dm_message = (
        "Ваше сообщение было удалено. Пожалуйста, соблюдайте структуру сообщений канала. "
        "Используйте команду `&team_help` для получения сведений."
    )

    # Логируем в канал LOG_CHANNEL_ID
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        print(f"❌ Не удалось найти канал с ID {LOG_CHANNEL_ID} для логов.")
        return

    try:
        # Отправляем ЛС пользователю
        await user.send(dm_message)

        # Логируем информацию о сообщении
        log_message = (
            f"{user.mention}, ваше сообщение было удалено. "
            "Пожалуйста, соблюдайте правила и структуру канала. "
            "Используйте `&team_help` для получения инструкций."
        )
        await log_channel.send(log_message)

        # Логируем причину удаления
        log_message = (
            f"❌ Сообщение пользователя `{user.mention}` "
            f"было удалено в канале {message.channel.mention}. "
            "Причина: нарушение правил."
        )
        await log_channel.send(log_message)

    except disnake.Forbidden:
        # Если не удается отправить ЛС (например, заблокировали бота)
        await log_channel.send(
            f"⚠️ Не удалось отправить ЛС пользователю {user.mention}."
        )


async def handle_mention(message):
    """
    Обрабатывает упоминания бота и отвечает на определённые фразы.
    """
    text_without_mention = message.content.replace(
        f"<@{bot.user.id}>", ""
    ).strip()
    data = JsonData()

    # Проверяем вариации фраз из JsonData
    for variation in data.get_data("hug_variations"):
        if fuzz.token_sort_ratio(text_without_mention.lower(), variation) > 80:
            await message.channel.send("*Обнимает в ответ.*")
            break


async def handle_github_pattern(message):
    """
    Проверяет наличие шаблона GitHub issue/PR в сообщении и отправляет ссылку на него.
    """
    match = re.search(r"\[(n|o)(\d+)\]", message.content)
    if match:
        repo_code, number = match.groups()
        link = await get_github_link(repo_code, number)
        if link:
            await message.channel.send(link)


async def get_github_link(repo_code, number):
    """
    Проверяет существование GitHub issue или PR и возвращает ссылку.
    """
    repo_name = REPOSITORIES.get(repo_code)
    if not repo_name:
        print(f"⚠️ Репозиторий с кодом {repo_code} не найден.")
        return None

    base_api_url = f"https://api.github.com/repos/{AUTHOR}/{repo_name}"
    issue_url = f"{base_api_url}/issues/{number}"
    pr_url = f"{base_api_url}/pulls/{number}"

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


async def send_ahat_message_post(message):
    """
    Если в логах а-чата замечено сообщение от пользователя
    Создается пост запрос, и отправляется в игру
    """
    if message.author.id == 1309279443943948328: # Игнорим ВэбХукк
        return

    # url = f"http://{ADDRESS_DEV}:1211/admin/actions/a_chat" # DEV
    url = f"http://{ADDRESS_MRP}:1212/admin/actions/a_chat"

    post_data = {
        "Message": f"{message.content}",
        "NickName": f"{message.author.name}"
    }

    try:
        response = requests.post(url, json=post_data, headers=POST_ADMIN_HEADERS, timeout=5)
        response.raise_for_status()  # Если статус код 4xx или 5xx, будет сгенерировано исключение
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    else:
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
