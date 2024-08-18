import discord
from github_processor import (create_embed_list, fetch_github_data,
                              send_embeds, validate_repository, validate_user)

from bot_init import bot


@bot.command(name='review')
async def review(ctx, repo_key: str):
    if not await validate_user(ctx):
        return

    repository_name = await validate_repository(ctx, repo_key)
    if not repository_name:
        return

    url = f"https://api.github.com/repos/{repository_name}/pulls"
    pulls = await fetch_github_data(url, {"state": "open", "sort": "created", "base": "master"})

    if not pulls:
        await ctx.send("Пулл-реквесты не найдены или не требуют ревью.")
        return

    pull_requests_list = [
        {
            "title": pr['title'],
            "url": pr['html_url'],
            "author": pr['user']['login'],
            "requested_by": [reviewer['login'] for reviewer in pr.get('requested_reviewers', [])]
        }
        for pr in pulls if any(label['name'] == "Status: Needs Review" for label in pr['labels'])
    ]

    embed_list = await create_embed_list(
        f"Список пулл-реквестов для ревью. \nРепозиторий: {repository_name}",
        pull_requests_list,
        discord.Color.dark_red(),
        lambda pr: {
            "name": pr['title'],
            "value": f"Автор: {pr['author']}\nЧьё ревью запрошено: {', '.join(pr['requested_by']) if pr['requested_by'] else 'Нет запрашиваемых рецензентов'}\nСсылка: {pr['url']}",
            "inline": False
        }
    )

    await send_embeds(ctx, embed_list)