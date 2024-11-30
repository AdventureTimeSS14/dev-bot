import re
from datetime import datetime, timezone

import discord
from discord.ext import tasks

from bot_init import bot
from config import (AUTHOR, CHANGELOG_CHANNEL_ID, REPOSITORIES,
                    SECOND_UPDATE_CHANGELOG)

from .github_processor import fetch_github_data

LCT: datetime = None


@tasks.loop(seconds=SECOND_UPDATE_CHANGELOG)
async def fetch_merged_pull_requests():
    global LCT
    url = (
        f'https://api.github.com/repos/{AUTHOR}/{REPOSITORIES["n"]}/pulls?state=closed'
    )
    pull_requests = await fetch_github_data(
        url, {"Accept": "application/vnd.github.v3+json"}
    )

    if not pull_requests:
        print("Pull requests not found or an error occured")
        return
    for pr in pull_requests:
        merged_at = pr.get("merged_at")
        if not pr["merged_at"]:
            continue

        merged_at = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )

        if LCT and merged_at > LCT:
            pr_title = pr["title"]
            pr_url = pr["html_url"]
            description = pr.get("body", "")
            author_name = pr["user"]["login"]
            description = re.sub(
                r"<!--.*?-->", "", description, flags=re.DOTALL
            ).strip()
            match = re.search(r"(:cl:.*?)(\n|$)", description, re.DOTALL)

            if not match:
                continue

            cl_text = match.group(1).strip()
            remaining_lines = description[match.end() :].strip()
            description = (
                f"{cl_text}\n{remaining_lines}" if remaining_lines else cl_text
            )

            embed = discord.Embed(
                title=f"Пулл-реквест замержен: {pr_title}",
                color=discord.Color.dark_green(),
            )
            embed.add_field(name="Изменения:", value=description, inline=False)
            embed.add_field(name="Автор:", value=author_name, inline=False)
            pr_number = pr["number"]  # Получаем номер PR
            embed.add_field(name="Ссылка:", value=f"[PR #{pr_number}]({pr_url})", inline=False)

            channel = bot.get_channel(CHANGELOG_CHANNEL_ID)
            if channel is None:
                print(f"Channel with ID {CHANGELOG_CHANNEL_ID} not found.")
                return

            await channel.send(embed=embed)

    LCT = datetime.now(timezone.utc)
