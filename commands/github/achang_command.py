import discord
from discord.ext import commands

from bot_init import bot

from .github_processor import (create_embed_list, fetch_github_data,
                               send_embeds, validate_repository, validate_user)


@bot.command(name='achang')
async def achang(ctx, repo_key: str):
    if not await validate_user(ctx):
        return

    repository_name = await validate_repository(ctx, repo_key)
    if not repository_name:
        return

    url = f"https://api.github.com/repos/{repository_name}/pulls"
    pulls = await fetch_github_data(url, {"state": "open", "sort": "created", "base": "master"})

    if not pulls:
        await ctx.send("Пулл-реквесты не найдены или не требуют изменений.")
        return

    pull_requests_list = [
        {
            "title": pr['title'],
            "url": pr['html_url'],
            "author": pr['user']['login'],
            "requested_by": [reviewer['login'] for reviewer in pr.get('requested_reviewers', [])]
        }
        for pr in pulls if any(label['name'] == "Status: Awaiting Changes" for label in pr['labels'])
    ]

    embed_list = await create_embed_list(
        f"Список пулл-реквестов, требующих изменений. \nРепозиторий: {repository_name}",
        pull_requests_list,
        discord.Color.dark_gold(),
        lambda pr: {
            "name": pr['title'],
            "value": f"Автор: {pr['author']}\nЧьё ревью запрошено: {', '.join(pr['requested_by']) if pr['requested_by'] else 'Нет запрашиваемых рецензентов'}\nСсылка: {pr['url']}",
            "inline": False
        }
    )

    await send_embeds(ctx, embed_list)
    
@achang.error
async def achang_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Вы не указали ключ к репозиторию. Указать ключ к репозиторию можно следующим образом: `&achang n`, `&achang o`")
