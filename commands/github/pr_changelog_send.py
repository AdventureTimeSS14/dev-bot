import re
from datetime import datetime, timezone

import discord
import requests
from discord.ext import commands

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import AUTHOR, CHANGELOG_CHANNEL_ID, REPOSITORIES, WHITELIST_ROLE_ID

MAX_FIELD_LENGTH = 1024  # Максимальный размер поля для Embed


def smart_truncate(text, max_length):
    """Умная обрезка текста: обрезает до максимальной длины, не разрывая слова или предложения."""
    if len(text) <= max_length:
        return text

    # Ищем последнее завершенное предложение перед обрезкой
    truncated_text = text[:max_length]
    last_period = truncated_text.rfind(".")

    if last_period == -1:  # Если нет точки, обрезаем просто по лимиту
        truncated_text = truncated_text[:max_length]
    else:
        truncated_text = truncated_text[: last_period + 1]

    return truncated_text.strip() + "..."  # Добавляем многоточие


@bot.command(
    name="pr",
    help="Получить информацию о замерженном пулл-реквесте по его номеру.",
)
@has_any_role_by_id(
    WHITELIST_ROLE_ID
)  # Проверяем, есть ли у пользователя доступ к выполнению команды
async def get_pr_info(ctx, pr_number: int):
    """
    Команда для получения информации о замерженном пулл-реквесте из GitHub.
    """
    # Формируем URL для запроса данных о пулл-реквесте
    url = f'https://api.github.com/repos/{AUTHOR}/{REPOSITORIES["n"]}/pulls/{pr_number}'
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        # Выполняем запрос к API GitHub
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        pr = response.json()
    except requests.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса к GitHub API: {e}")
        await ctx.send("❌ Пулл-реквест не найден или произошла ошибка.")
        return

    # Проверяем, был ли пулл-реквест замержен
    if not pr.get("merged_at"):
        await ctx.send("❌ Этот пулл-реквест не был замержен.")
        return

    # Извлекаем данные о пулл-реквесте
    merged_at = datetime.strptime(
        pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)
    pr_title = pr["title"]
    pr_url = pr["html_url"]
    description = pr.get("body", "").strip()
    author_name = pr["user"]["login"]

    # Получаем данные о соавторах, если они есть
    coauthors = pr.get("coauthors", [])

    # Очищаем описание от комментариев и ищем текст изменений
    description = re.sub(r"<!--.*?-->", "", description, flags=re.DOTALL)
    match = re.search(r"(:cl:.*?|\U0001F191.*?)(\n|$)", description, re.DOTALL)

    if not match:
        await ctx.send("❌ Не удалось найти описание изменений.")
        return

    cl_text = match.group(1).strip()
    remaining_lines = description[match.end() :].strip()
    description = (
        f"{cl_text}\n{remaining_lines}" if remaining_lines else cl_text
    )

    # Умная обрезка текста, если описание слишком длинное
    description = smart_truncate(description, MAX_FIELD_LENGTH)

    # Формируем Embed для отображения данных
    embed = discord.Embed(
        title=f"Пулл-реквест замержен: {pr_title}",
        color=discord.Color.dark_green(),
        timestamp=merged_at,
    )

    # Добавляем поля в Embed
    embed.add_field(name="Изменения:", value=description, inline=False)
    embed.add_field(name="Автор:", value=author_name, inline=False)
    embed.add_field(
        name="Ссылка:", value=f"[PR #{pr_number}]({pr_url})", inline=False
    )

    # Добавляем соавторов, если они есть
    if coauthors:
        coauthors_str = "\n".join(coauthors)
        embed.add_field(name="Соавторы:", value=coauthors_str, inline=False)

    embed.set_footer(text="Дата мержа")

    # Отправляем Embed в канал с changelog
    channel = bot.get_channel(CHANGELOG_CHANNEL_ID)
    if channel is None:
        await ctx.send(f"❌ Канал с ID {CHANGELOG_CHANNEL_ID} не найден.")
        return

    try:
        await channel.send(embed=embed)
        await ctx.send(
            f"Информация о пулл-реквесте успешно отправлена в канал <#{CHANGELOG_CHANNEL_ID}>."
        )
    except discord.Forbidden:
        await ctx.send(
            "❌ У бота нет прав для отправки сообщений в указанный канал."
        )
    except discord.HTTPException as e:
        print(f"❌ Ошибка при отправке Embed: {e}")
        await ctx.send(
            "❌ Произошла ошибка при отправке информации о пулл-реквесте."
        )
