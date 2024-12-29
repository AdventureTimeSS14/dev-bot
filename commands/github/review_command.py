import discord
from discord.ext import commands

from commands.github.utils import validate_and_return_if_invalid
from bot_init import bot
from .github_processor import (
    create_embed_list,
    fetch_github_data,
    send_embeds,
    validate_repository,
)


@bot.command(
    name="review",
    help="Получает список пулл-реквестов для ревью из указанного репозитория.",
)
async def review(ctx, repo_key: str):
    """
    Команда для получения списка пулл-реквестов, которые требуют ревью, из указанного репозитория.
    """
    # Проверяем, имеет ли пользователь доступ к выполнению команды
    if not await validate_and_return_if_invalid(ctx):
        return

    # Проверяем репозиторий по переданному ключу
    repository_name = await validate_repository(ctx, repo_key)
    if not repository_name:
        return

    # Формируем URL API GitHub для получения пулл-реквестов
    url = f"https://api.github.com/repos/{repository_name}/pulls"
    pulls = await fetch_github_data(
        url,
        {"state": "open", "sort": "created", "base": "master"},
    )

    # Если пулл-реквесты не найдены
    if not pulls:
        await ctx.send("❌ Пулл-реквесты не найдены или не требуют ревью.")
        return

    # Формируем список пулл-реквестов с меткой "Status: Needs Review"
    pull_requests_list = [
        {
            "title": pr["title"],
            "url": pr["html_url"],
            "author": pr["user"]["login"],
            "requested_by": [
                reviewer["login"]
                for reviewer in pr.get("requested_reviewers", [])
            ],
        }
        for pr in pulls
        if any(
            label["name"] == "Status: Needs Review" for label in pr["labels"]
        )
    ]

    # Если нет пулл-реквестов с меткой "Status: Needs Review"
    if not pull_requests_list:
        await ctx.send("❌ Нет пулл-реквестов с меткой `Status: Needs Review`. ")
        return

    # Создаём Embed-список для отображения в Discord
    embed_list = await create_embed_list(
        f"📋 Список пулл-реквестов для ревью.\nРепозиторий: `{repository_name}`",
        pull_requests_list,
        discord.Color.dark_red(),
        lambda pr: {
            "name": pr["title"],
            "value": (
                f"**Автор:** {pr['author']}\n"
                f"**Чьё ревью запрошено:** {', '.join(pr['requested_by']) if pr['requested_by'] else 'Нет запрашиваемых рецензентов'}\n" # pylint: disable=C0301
                f"**Ссылка:** [Открыть PR]({pr['url']})"
            ),
            "inline": False,
        },
    )

    # Отправляем список Embed-ов
    await send_embeds(ctx, embed_list)


@review.error
async def review_error(ctx, error):
    """
    Обработчик ошибок для команды review.
    """
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "❌ Вы не указали ключ к репозиторию. Укажите ключ к репозиторию следующим образом:\n"
            "`&review n` или `&review o`."
        )
    else:
        # Логируем и отправляем сообщение об ошибке
        print(f"❌ Ошибка в команде review: {error}")
        await ctx.send(
            "❌ Произошла ошибка при выполнении команды. Проверьте логи для подробностей."
        )
