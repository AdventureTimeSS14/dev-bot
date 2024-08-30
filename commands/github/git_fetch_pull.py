import re
import requests
from datetime import datetime
from config import CHANGELOG_CHANNEL_ID, GITHUB, SECOND_UPDATE_CHANGELOG, AUTHOR, REPOSITORIES
import discord
from discord.ext import tasks

from bot_init import bot

@tasks.loop(seconds=SECOND_UPDATE_CHANGELOG)
async def fetch_merged_pull_requests():
    headers = {
        'Authorization': f'token {GITHUB}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    last_checked_time = datetime.utcnow()

    response = requests.get(f'https://api.github.com/repos/{AUTHOR}/{REPOSITORIES["n"]}/pulls?state=closed', headers=headers)
    if response.status_code == 200:
        pull_requests = response.json()
        for pr in pull_requests:
            if pr['merged_at']:
                merged_at = datetime.strptime(pr['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
                if merged_at > last_checked_time:  # Проверяем, был ли PR замержен после последней проверки
                    pr_title = pr['title']
                    pr_url = pr['html_url']
                    description = pr.get('body', "Нет описания") 
                    author_name = pr['user']['login']
                    
                    # Удаляем HTML-комментарии из описания
                    description = re.sub(r'<!--.*?-->', '', description, flags=re.DOTALL).strip()
                    
                    # Ищем :cl: и все, что идет после него
                    match = re.search(r'(:cl:.*?)(\n|$)', description, re.DOTALL)
                    if match:
                        cl_text = match.group(1).strip()
                        
                        remaining_lines = description[match.end():].strip()
                        
                        if remaining_lines:
                            description = f"{cl_text}\n{remaining_lines}"
                        else:
                            description = cl_text
                        
                        embed = discord.Embed(
                            title=f'Пулл-реквест замержен: {pr_title}',
                            color=discord.Color.dark_green()
                        )
                        embed.add_field(name='Изменения:', value=description, inline=False)
                        embed.add_field(name='Ссылка:', value=f'[PR]({pr_url})', inline=False)

                        channel = bot.get_channel(CHANGELOG_CHANNEL_ID)
                        await channel.send(embed=embed)

        last_checked_time = datetime.utcnow()
