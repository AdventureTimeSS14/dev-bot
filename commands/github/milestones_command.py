import discord
from discord.ext import commands

from bot_init import bot

from .github_processor import (
    create_embed_list,
    fetch_github_data,
    send_embeds,
    validate_repository,
    validate_user,
)


@bot.command(name="milestones")
async def milestones(ctx, repo_key: str):
    if not await validate_user(ctx):
        return

    repository_name = await validate_repository(ctx, repo_key)
    if not repository_name:
        return

    url = f"https://api.github.com/repos/{repository_name}/milestones"
    milestones = await fetch_github_data(url)

    if not milestones:
        await ctx.send("Milestones не найдены.")
        return

    milestones_list = [
        {
            "title": milestone["title"],
            "url": milestone["url"],
            "due_date": milestone["due_on"],
            "completion": (
                f"{(milestone['closed_issues'] / (milestone['open_issues'] + milestone['closed_issues'])) * 100:.2f}%"
                if milestone["open_issues"] + milestone["closed_issues"] > 0
                else "0%"
            ),
            "open_issues": milestone["open_issues"],
            "closed_issues": milestone["closed_issues"],
        }
        for milestone in milestones
    ]

    embed_list = await create_embed_list(
        f"Список Milestones. \nРепозиторий: {repository_name}",
        milestones_list,
        discord.Color.blue(),
        lambda milestone: {
            "name": milestone["title"],
            "value": f"Ссылка: {milestone['url']}\nДата завершения: {milestone['due_date']}\nЗакрытые задачи: {milestone['closed_issues']}\nОткрытые задачи: {milestone['open_issues']}\nПроцент выполнения: {milestone['completion']}",
            "inline": False,
        },
    )

    await send_embeds(ctx, embed_list)


@milestones.error
async def milestones_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Вы не указали ключ к репозиторию. "
            "Указать ключ к репозиторию можно следующим "
            "образом: `&milestones n`, `&milestones o`"
        )
