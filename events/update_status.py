from datetime import datetime, timezone
from urllib.parse import urlparse, urlunparse

import aiohttp
import dateutil.parser
import discord
from discord.ext import commands, tasks

from bot_init import bot
from config import CHANNEL_ID_UPDATE_STATUS, SS14_ADDRESS

# Определение уровней игры для SS14
SS14_RUN_LEVELS = {
    0: "Лобби",
    1: "Раунд идёт",
    2: "Окончание раунда..."
}

@tasks.loop(seconds=15)
async def update_status():
    """
    Обновление Rich Presence бота.
    """
    status_data = await get_ss14_server_status_second(SS14_ADDRESS)
    if not status_data:
        await bot.change_presence(activity=discord.Game(name="Ошибка при получении статуса"))
        return

    # Формируем строку для статуса
    count = status_data.get("players", "?")
    countmax = status_data.get("soft_max_players", "?")
    name = status_data.get("name", "Неизвестно")
    preset = status_data.get("preset", "?")
    round_id = status_data.get("round_id", "?")
    run_level = SS14_RUN_LEVELS.get(status_data.get("run_level"), "Неизвестно")

    status_state = f"Игроков: {count}/{countmax} | Режим: {preset} | Раунд: {round_id} | Статус: {run_level}"
    activity = discord.Activity(type=discord.ActivityType.playing, name=name, state=status_state)
    await bot.change_presence(activity=activity)

@tasks.loop(seconds=50)
async def update_status_server_message_edit():
    """
    Фоновая задача для обновления статуса сервера в сообщении.
    """
    channel = bot.get_channel(CHANNEL_ID_UPDATE_STATUS)
    if channel is None:
        print("Не удалось найти канал!")
        return

    try:
        message = await channel.fetch_message(1320771122433622084)
        status_data = await get_ss14_server_status_second(SS14_ADDRESS)

        if not status_data:
            embed = create_error_embed(SS14_ADDRESS)
        else:
            embed = create_status_embed(SS14_ADDRESS, status_data)

        await message.edit(embed=embed)

    except discord.NotFound:
        print("Сообщение не найдено!")
    except discord.Forbidden:
        print("У бота нет прав для редактирования сообщения!")
    except Exception as e:
        print(f"Ошибка при обновлении сообщения: {e}")

async def get_ss14_server_status_second(address: str) -> dict:
    """
    Получает статус игры с сервера SS14.
    """
    url = get_ss14_status_url(address)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url + "/status") as resp:
                if resp.status != 200:
                    raise Exception(f"HTTP статус {resp.status}")
                return await resp.json()
    except Exception as e:
        print(f"Ошибка при получении статуса с сервера SS14: {e}")
        return None

def get_ss14_status_url(url: str) -> str:
    """
    Преобразует адрес сервера в корректный URL.
    """
    if url.startswith("ss14://"):
        url = "http://" + url[7:]  # Убираем ss14:// и добавляем http://

    parsed = urlparse(url, allow_fragments=False)
    port = parsed.port or 1212  # Если порт не указан, используем 1212
    return urlunparse(("http", f"{parsed.hostname}:{port}", parsed.path, "", "", ""))

def create_status_embed(address: str, status_data: dict, author=None) -> discord.Embed:
    """
    Создаёт Embed с информацией о статусе сервера.
    """
    embed = discord.Embed(color=discord.Color.dark_blue())
    embed.title = status_data.get("name", "Неизвестно")
    embed.set_footer(text=f"Адрес: {address}")

    count = status_data.get("players", "?")
    countmax = status_data.get("soft_max_players", "?")
    round_id = status_data.get("round_id", "?")
    gamemap = status_data.get("map", "Неизвестно")
    preset = status_data.get("preset", "?")
    rlevel = status_data.get("run_level", None)
    bunker = status_data.get("panic_bunker", "Неизвестно")
    bunker = "Включен" if bunker else "Отключен"
    run_level = SS14_RUN_LEVELS.get(rlevel, "Неизвестно")

    # Добавляем поля
    embed.add_field(name="Игроков", value=f"{count}/{countmax}", inline=False)
    embed.add_field(name="Раунд", value=round_id, inline=False)
    embed.add_field(name="Карта", value=gamemap, inline=False)
    embed.add_field(name="Режим игры", value=preset, inline=False)
    embed.add_field(name="Статус", value=run_level, inline=False)
    embed.add_field(name="Бункер", value=bunker, inline=False)

    # Добавляем время раунда, если оно есть
    starttimestr = status_data.get("round_start_time")
    if starttimestr:
        starttime = dateutil.parser.isoparse(starttimestr)
        delta = datetime.now(timezone.utc) - starttime
        time_str = []
        if delta.days > 0:
            time_str.append(f"{delta.days} дней")
        hours, minutes = divmod(delta.seconds, 3600)
        if hours > 0:
            time_str.append(f"{hours} часов")
        time_str.append(f"{minutes // 60} минут")
        embed.add_field(name="Время раунда", value=", ".join(time_str), inline=False)

    if author:
        embed.set_author(name=author.name, icon_url=author.avatar.url)

    return embed

def create_error_embed(address: str) -> discord.Embed:
    """
    Создаёт Embed для ошибок.
    """
    embed = discord.Embed(color=discord.Color.red())
    embed.title = "Ошибка получения данных"
    embed.set_footer(text=f"Адрес: {address}")

    fields = ["Игроков", "Статус", "Время раунда", "Раунд", "Карта", "Режим игры", "Бункер"]
    for field in fields:
        embed.add_field(name=field, value="Error!", inline=False)

    return embed
