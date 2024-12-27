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


@bot.command(name="forks")
async def forks(ctx, repo_key: str):
    """
    Команда для получения списка форков заданного репозитория.
    """
    # Проверяем доступ пользователя
    if not await validate_user(ctx):
        return

    # Проверяем валидность ключа репозитория
    repository_name = await validate_repository(ctx, repo_key)
    if not repository_name:
        return

    # Формируем URL и запрашиваем данные о форках
    url = f"https://api.github.com/repos/{repository_name}/forks"
    forks = await fetch_github_data(url)

    if not forks:
        await ctx.send("❌ Форки не найдены.")
        return

    # Формируем список форков
    forks_list = [
        {
            "name": fork["full_name"],
            "owner": fork["owner"]["login"],
            "url": fork["html_url"],
        }
        for fork in forks
    ]

    # Создаём список Embed-сообщений
    embed_list = await create_embed_list(
        title=f"🌳 Список форков для репозитория {repository_name}",
        items=forks_list,
        color=discord.Color.dark_green(),
        formatter=lambda fork: {
            "name": fork["name"],
            "value": f"Владелец: {fork['owner']}\nСсылка: [Открыть форк]({fork['url']})",
            "inline": False,
        },
    )

    # Отправляем Embed-сообщения
    await send_embeds(ctx, embed_list)


@forks.error
async def forks_error(ctx, error):
    """
    Обработчик ошибок команды forks.
    """
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "❌ Вы не указали ключ к репозиторию.\n"
            "Укажите ключ следующим образом: `&forks n` или `&forks o`."
        )
    else:
        await ctx.send(
            "❌ Произошла ошибка при выполнении команды. Пожалуйста, попробуйте позже."
        )
