import discord
from discord.ext import commands
import re
from datetime import datetime, timezone
import requests

from bot_init import bot

from .github_processor import (create_embed_list, fetch_github_data,
                               send_embeds, validate_repository, validate_user)

from config import (AUTHOR, CHANGELOG_CHANNEL_ID, REPOSITORIES)

from .github_processor import fetch_github_data

LCT: datetime = None

@bot.command(name='pr')
async def get_pr_info(ctx, pr_number: int):
    if ctx.author.id != 328502766622474240:
        await ctx.send("У вас нет доступа к этой команде.")
        return
        
    url = f'https://api.github.com/repos/{AUTHOR}/{REPOSITORIES["n"]}/pulls/{pr_number}'
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        await ctx.send("Пулл-реквест не найден или произошла ошибка.")
        return
    
    pr = response.json()
    
    if not pr.get("merged_at"):
        await ctx.send("Этот пулл-реквест не был замержен.")
        return

    merged_at = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    pr_title = pr["title"]
    pr_url = pr["html_url"]
    description = pr.get("body", "")
    author_name = pr["user"]["login"]
    
    description = re.sub(r"<!--.*?-->", "", description, flags=re.DOTALL).strip()
    match = re.search(r"(:cl:.*?)(\n|$)", description, re.DOTALL)

    if not match:
        await ctx.send("Не удалось найти описание изменений.")
        return

    cl_text = match.group(1).strip()
    remaining_lines = description[match.end():].strip()
    description = f"{cl_text}\n{remaining_lines}" if remaining_lines else cl_text

    embed = discord.Embed(
        title=f"Пулл-реквест замержен: {pr_title}",
        color=discord.Color.dark_green(),
    )
    embed.add_field(name="Изменения:", value=description, inline=False)
    embed.add_field(name="Автор:", value=author_name, inline=False)
    embed.add_field(name="Ссылка:", value=f"[PR]({pr_url})", inline=False)

    channel = bot.get_channel(CHANGELOG_CHANNEL_ID)
    if channel is None:
        await ctx.send(f"Канал с ID {CHANGELOG_CHANNEL_ID} не найден.")
        return

    await channel.send(embed=embed)