import asyncio
import time
import logging
from datetime import timedelta, timezone, datetime
import aiohttp
import discord
from discord.ext import tasks, commands
from bot_init import bot
from urllib.parse import urlparse, urlunparse
import dateutil.parser

# Определение уровней игры для SS14
SS14_RUN_LEVEL_PREGAME = 0
SS14_RUN_LEVEL_GAME = 1
SS14_RUN_LEVEL_POSTGAME = 2

@bot.command(name='status')
async def get_status_command(ctx):
    """
    Команда для получения статуса сервера SS14 в чате Discord с подробным выводом через Embed.
    """
    ss14_address = "ss14://193.164.18.155"
    
    # Формируем URL для получения данных о сервере
    url = get_ss14_status_url(ss14_address)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url + "/status") as resp:
                # Получаем данные о статусе сервера
                json = await resp.json()

        # Создаём Embed сообщение для вывода информации
        embed = discord.Embed(color=discord.Color.dark_blue())  # Синий цвет

        # Извлекаем информацию о сервере
        count = json.get("players", "?")
        countmax = json.get("soft_max_players", "?")
        name = json.get("name", "Неизвестно")
        round_id = json.get("round_id", "?")
        gamemap = json.get("map", "?")
        preset = json.get("preset", "?")
        rlevel = json.get("run_level", None)

        # Устанавливаем заголовок Embed
        embed.title = name
        embed.set_footer(text=f"Адрес: {ss14_address}")

        # Добавляем количество игроков
        embed.add_field(name="Игроков", value=f"{count}/{countmax}", inline=False)

        # Определяем статус сервера по run_level
        if rlevel is not None:
            status = "Неизвестно"
            if rlevel == SS14_RUN_LEVEL_PREGAME:
                status = "Лобби"
            elif rlevel == SS14_RUN_LEVEL_GAME:
                status = "Раунд идёт"
            elif rlevel == SS14_RUN_LEVEL_POSTGAME:
                status = "Окончание раунда..."

            embed.add_field(name="Статус", value=status, inline=False)

        # Добавляем время раунда, если оно есть
        starttimestr = json.get("round_start_time")
        if starttimestr:
            starttime = dateutil.parser.isoparse(starttimestr)
            delta = datetime.now(timezone.utc) - starttime
            time_str = []
            if delta.days > 0:
                time_str.append(f"{delta.days} дней")
            minutes = delta.seconds // 60
            hours = minutes // 60
            if hours > 0:
                time_str.append(f"{hours} часов")
                minutes %= 60
            time_str.append(f"{minutes} минут")

            embed.add_field(name="Время раунда", value=", ".join(time_str), inline=False)

        # Добавляем другие поля
        embed.add_field(name="Раунд", value=round_id, inline=False)
        embed.add_field(name="Карта", value=gamemap, inline=False)
        embed.add_field(name="Режим игры", value=preset, inline=False)

        # Отправляем Embed сообщение в канал
        await ctx.send(embed=embed)

    except Exception as e:
        print(f"Ошибка при получении статуса с сервера SS14: {e}")
        await ctx.send("Ошибка при получении статуса с сервера.")

@tasks.loop(seconds=2)  # Обновляем статус каждую секунду или две
async def update_status():
    if not hasattr(bot, 'start_time') or bot.start_time is None:
        return  # Если время старта не задано, пропускаем обновление
    # Закомментировано обновление времени работы бота
    # # Вычисляем прошедшее время с момента старта
    # elapsed_time = time.time() - bot.start_time
    # elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))
    # # Оставшееся время до отключения
    # remaining_time = (5 * 3600 + 57 * 60) - elapsed_time
    # remaining_time_str = str(timedelta(seconds=int(remaining_time)))

    ss14_address = "ss14://193.164.18.155"
    url = get_ss14_status_url(ss14_address)
    
    try:
        # Получаем статус с сервера SS14
        async with aiohttp.ClientSession() as session:
            async with session.get(url + "/status") as resp:
                json = await resp.json()

        # Извлекаем данные о статусе сервера
        count = json.get("players", "?")
        countmax = json.get("soft_max_players", "?")
        name = json.get("name", "Неизвестно")
        rlevel = json.get("run_level", None)
        round_id = json.get("round_id", "?")
        preset = json.get("preset", "?")

        # Определяем статус сервера по run_level
        status = "Неизвестно"
        if rlevel == SS14_RUN_LEVEL_PREGAME:
            status = "Лобби"
        elif rlevel == SS14_RUN_LEVEL_GAME:
            status = "Раунд идёт"
        elif rlevel == SS14_RUN_LEVEL_POSTGAME:
            status = "Окончание раунда..."

        # Формируем строку для статуса бота
        status_state = f"Игроков: {count}/{countmax} | Режим: {status} | Раунд: {round_id}"  # Мелким шрифтом

        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name=name,
            state=status_state
        )
        # Обновляем статус бота
        await bot.change_presence(activity=activity)

    except Exception as e:
        print(f"Ошибка при получении статуса с сервера SS14: {e}")
        await bot.change_presence(activity=discord.Game(name="Ошибка при получении статуса"))

async def get_ss14_server_status(address: str) -> str:
    """
    Получает статус игры с сервера SS14 по адресу.
    """
    # Формируем правильный URL
    url = get_ss14_status_url(address)
    print(f"Запрос статуса SS14 на {url}")

    # Получаем статус сервера
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url + "/status") as resp:
                json = await resp.json()

        # Извлекаем данные о текущем статусе сервера
        count = json.get("players", "?")
        countmax = json.get("soft_max_players", "?")
        name = json.get("name", "Неизвестно")
        rlevel = json.get("run_level")

        # Статус сервера
        status = "Неизвестно"
        if rlevel == SS14_RUN_LEVEL_PREGAME:
            status = "Лобби"
        elif rlevel == SS14_RUN_LEVEL_GAME:
            status = "Раунд идёт"
        elif rlevel == SS14_RUN_LEVEL_POSTGAME:
            status = "Окончание раунда..."

        # Формируем сообщение статуса
        return f"{name} | Игроков: {count}/{countmax} | Статус: {status}"

    except Exception as e:
        print(f"Ошибка при получении статуса с сервера SS14: {e}")
        return "Ошибка при получении статуса"
    
def get_ss14_status_url(url: str) -> str:
    """
    Преобразует адрес сервера в правильный URL с учетом схемы.
    """
    # Преобразуем из ss14:// в http(s)://
    if url.startswith("ss14://"):
        url = "http://" + url[7:]  # Убираем префикс ss14:// и добавляем http://

    parsed = urlparse(url, allow_fragments=False)

    port = parsed.port
    if not port:
        port = 1212  # Устанавливаем стандартный порт 1212

    scheme = "http"

    return urlunparse((scheme, f"{parsed.hostname}:{port}", parsed.path, parsed.params, parsed.query, parsed.fragment))
