import discord
from github_processor import (create_embed_list, fetch_github_data,
                              send_embeds, validate_repository, validate_user)

from bot_init import bot


@bot.command(name='forks')
async def forks(ctx, repo_key: str):
    if not await validate_user(ctx):
        return

    repository_name = await validate_repository(ctx, repo_key)
    if not repository_name:
        return

    url = f"https://api.github.com/repos/{repository_name}/forks"
    forks = await fetch_github_data(url)

    if not forks:
        await ctx.send("Форки не найдены.")
        return

    forks_list = [
        {
            "name": fork['full_name'],
            "owner": fork['owner']['login'],
            "url": fork['html_url']
        }
        for fork in forks
    ]

    embed_list = await create_embed_list(
        f"Список форков для репозитория {repository_name}",
        forks_list,
        discord.Color.dark_green(),
        lambda fork: {
            "name": fork['name'],
            "value": f"Владелец: {fork['owner']}\nСсылка: {fork['url']}",
            "inline": False
        }
    )

    await send_embeds(ctx, embed_list)

