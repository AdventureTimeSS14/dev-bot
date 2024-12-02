import re

import requests
from fuzzywuzzy import fuzz

from bot_init import bot
from config import AUTHOR, GLOBAL_SESSION, REPOSITORIES, MY_USER_ID
from data import JsonData


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return
    
    # ну типо давай так
    specific_user_id = MY_USER_ID
    if message.mentions or message.reference and message.reference.resolved and message.reference.resolved.author.id == specific_user_id:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, не беспокоить.")
        return
    
    if f"<@{bot.user.id}>" in message.content:
        text_without_mention = message.content.replace(f"<@{bot.user.id}>", "").strip()
        data = JsonData()
        for variation in data.get_data('hug_variations'):
            if fuzz.token_sort_ratio(text_without_mention.lower(), variation) > 80:
                await message.channel.send("*Обнимает в ответ.*")
                break
    
    # Search for GitHub issue/PR pattern and respond with the appropriate link
    match = re.compile(r'\[(n|o)(\d+)\]').search(message.content)
    if match:
        repo_code, number = match.groups()
        link = check_github_issue_or_pr(repo_code, number)
        if link:
            await message.channel.send(f'{link}')

def check_github_issue_or_pr(repo_code, number):
    repo_name = REPOSITORIES.get(repo_code)
    if not repo_name:
        return None

    base_api_url = f'https://api.github.com/repos/{AUTHOR}/{repo_name}'
    issue_url = f'{base_api_url}/issues/{number}'
    pr_url = f'{base_api_url}/pulls/{number}'

    try:
        pr_response = GLOBAL_SESSION.get(pr_url)
        if pr_response.status_code == 200:
            pr_data = pr_response.json()
            return f'[{repo_name} PR {number}]({pr_data["html_url"]})'

        issue_response = GLOBAL_SESSION.get(issue_url)
        if issue_response.status_code == 200:
            issue_data = issue_response.json()
            return f'[{repo_name} Issue {number}]({issue_data["html_url"]})'

    except requests.RequestException as e:
        print(f"Ошибка при проверке GitHub issue или PR: {e}")

    return None