import re
import requests
import asyncio
from datetime import datetime
from config import CHANGELOG_CHANNEL_ID, GITHUB
import discord
from discord.ext import commands

from bot_init import bot

from .github_processor import (create_embed_list, fetch_github_data,
                               send_embeds, validate_repository, validate_user)

REPO = 'AdventureTimeSS14/space_station_ADT'

async def fetch_merged_pull_requests():
    headers = {
        'Authorization': f'token {GITHUB}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    last_checked_time = datetime.utcnow()  # Время последней проверки

    while True:
        response = requests.get(f'https://api.github.com/repos/{REPO}/pulls?state=closed', headers=headers)
        if response.status_code == 200:
            pull_requests = response.json()
            for pr in pull_requests:
                if pr['merged_at']:
                    merged_at = datetime.strptime(pr['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
                    if merged_at > last_checked_time:  # Проверяем, был ли PR замержен после последней проверки
                        pr_title = pr['title']
                        pr_url = pr['html_url']
                        description = pr['body'] if pr['body'] else "Нет описания"
                        author_name = pr['user']['login']  # Получаем ник автора пулл-реквеста
                        
                        # Удаляем HTML-комментарии из описания
                        description = re.sub(r'<!--.*?-->', '', description, flags=re.DOTALL).strip()
                        
                        # Ищем :cl: и все, что идет после него
                        match = re.search(r'(:cl:.*?)(\n|$)', description, re.DOTALL)
                        if match:
                            # Получаем текст после :cl:
                            cl_text = match.group(1).strip()
                            
                            # Извлекаем все строки после :cl:
                            remaining_lines = description[match.end():].strip()
                            
                            # Объединяем текст :cl: с оставшимися строками
                            if remaining_lines:
                                description = f"{cl_text}\n{remaining_lines}"
                            else:
                                description = cl_text
                            
                            # Создаем Embed-сообщение
                            embed = discord.Embed(
                                title=f'Пулл-реквест замержен: **{pr_title}**',
                                color=discord.Color.dark_green()
                            )
                            embed.add_field(name='Изменения:', value=description, inline=False)
                            embed.add_field(name='Ссылка:', value=f'[PR]({pr_url})', inline=False)

                            channel = bot.get_channel(CHANGELOG_CHANNEL_ID)
                            await channel.send(embed=embed)

            last_checked_time = datetime.utcnow()  # Обновляем время последней проверки

        await asyncio.sleep(60)  # Проверять каждую минуту
