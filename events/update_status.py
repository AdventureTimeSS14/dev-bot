import asyncio
import time
import logging
from datetime import timedelta
import aiohttp
import discord
from discord.ext import tasks, commands
from bot_init import bot
from urllib.parse import urlparse, urlunparse

# Определение уровней игры для SS14
SS14_RUN_LEVEL_PREGAME = 0
SS14_RUN_LEVEL_GAME = 1
SS14_RUN_LEVEL_POSTGAME = 2

# Настройка команды
@bot.command(name='status')
async def get_status_command(ctx):
    """
    Команда для получения статуса сервера SS14 в чате Discord.
    """
    ss14_address = "ss14://193.164.18.155"
    status_message = await get_ss14_server_status(ss14_address)
    await ctx.send(status_message)

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

    # Получаем статус с сервера SS14
    ss14_address = "ss14://193.164.18.155"
    status_message = await get_ss14_server_status(ss14_address)

    # Обновляем статус бота (выводим только статус игры на сервере)
    await bot.change_presence(activity=discord.Game(
        name=status_message
    ))

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
