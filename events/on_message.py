import re

import disnake
import requests
import random

from fuzzywuzzy import fuzz
from bot_init import bot
from events.utils import get_github_link

from config import (
    ADMIN_TEAM,
    AUTHOR,
    GLOBAL_SESSION,
    LOG_CHANNEL_ID,
    REPOSITORIES,
    ADDRESS_MRP,
    POST_ADMIN_HEADERS,
)
from data import JsonData


@bot.event
async def on_message(message):
    """
    Обработчик сообщений бота.
    """
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return

    # Обработка команд
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    # Ответ на упоминание бота
    if f"<@{bot.user.id}>" in message.content:
        await call_mention(message)
        await handle_mention(message)
        return

    # Проверка сообщений в канале для удаления
    if message.channel.id == ADMIN_TEAM:
        await handle_message_deletion(message)

    if message.channel.id == 1309262152586235964:
        await send_ahat_message_post(message)

    # Проверка на шаблон GitHub issue/PR
    await handle_github_pattern(message)
    
    await check_time_transfer_with_fuzz(message)
    
    await isinstance_chat(message)


async def send_ahat_message_post(message):
    """
    Если в логах а-чата замечено сообщение от пользователя
    Создается пост запрос, и отправляется в игру
    """
    if message.author.id == 1309279443943948328: # Игнорим ВэбХукк
        return
    # url = f"http://{ADDRESS_DEV}:1211/admin/actions/a_chat" # DEV
    url = f"http://{ADDRESS_MRP}:1212/admin/actions/a_chat"
    post_data = {
        "Message": f"{message.content}",
        "NickName": f"{message.author.name}"
    }
    try:
        response = requests.post(url, json=post_data, headers=POST_ADMIN_HEADERS, timeout=5)
        response.raise_for_status()  # Если статус код 4xx или 5xx, будет сгенерировано исключение
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    else:
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

async def handle_message_deletion(message):
    """
    Обрабатывает удаление сообщений в определенном канале и логирует информацию.
    """
    await message.delete()

    user = message.author
    dm_message = (
        "Ваше сообщение было удалено. Пожалуйста, соблюдайте структуру сообщений канала. "
        "Используйте команду `&team_help` для получения сведений."
    )

    # Логируем в канал LOG_CHANNEL_ID
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        print(f"❌ Не удалось найти канал с ID {LOG_CHANNEL_ID} для логов.")
        return

    try:
        # Отправляем ЛС пользователю
        await user.send(dm_message)

        # Логируем информацию о сообщении
        log_message = (
            f"{user.mention}, ваше сообщение было удалено. "
            "Пожалуйста, соблюдайте правила и структуру канала. "
            "Используйте `&team_help` для получения инструкций."
        )
        await log_channel.send(log_message)

        # Логируем причину удаления
        log_message = (
            f"❌ Сообщение пользователя `{user.mention}` "
            f"было удалено в канале {message.channel.mention}. "
            "Причина: нарушение правил."
        )
        await log_channel.send(log_message)

    except disnake.Forbidden:
        # Если не удается отправить ЛС (например, заблокировали бота)
        await log_channel.send(
            f"⚠️ Не удалось отправить ЛС пользователю {user.mention}."
        )

async def call_mention(message):
    """
    Обрабатывает упоминания бота и отвечает на определённые фразы.
    """
    text_without_mention = message.content.replace(
        f"<@{bot.user.id}>", ""
    ).strip()
    data = JsonData()

    # Проверяем вариации фраз из JsonData
    for variation in data.get_data("call_bot"):
        if fuzz.token_sort_ratio(text_without_mention.lower(), variation) > 80:
            # Список возможных мурчаний
            meow_responses = [
                "Мурррр?",
                "Мрья?! >~<",
                "Мрррр",
                "Мря? Я здеся 😽",
                "Мррр, как я тебя услышала?! 😸",
                "Мррр, что за вкусняшки принес?",
                "Мяу, ну что, погладим меня? 😻",
                "Мррр, ты меня разбудил!",
                "Мяууууу, где моя вкусняшка?!",
                "Мррр, не трогай моё место на диване! >_<",
            ]

            # Выбираем случайный ответ из списка
            responce = random.choice(meow_responses)

            await message.channel.send(responce)
            break


async def handle_mention(message):
    """
    Обрабатывает упоминания бота и отвечает на определённые фразы.
    """
    text_without_mention = message.content.replace(
        f"<@{bot.user.id}>", ""
    ).strip()
    data = JsonData()

    # Проверяем вариации фраз из JsonData
    for variation in data.get_data("hug_variations"):
        if fuzz.token_sort_ratio(text_without_mention.lower(), variation) > 80:
            await message.channel.send("*Обнимает в ответ.*")
            break


async def handle_github_pattern(message):
    """
    Проверяет наличие шаблона GitHub issue/PR в сообщении и отправляет ссылку на него.
    """
    match = re.search(r"\[(n?|o)(\d+)\]", message.content)  # Добавлен необязательный префикс 'n'
    if match:
        repo_code, number = match.groups()
        # Если 'n' не найдено, то присваиваем 'n' по умолчанию
        repo_code = 'n' if not repo_code else repo_code
        embed_or_str = await get_github_link(repo_code, number)
        
        # Если получен embed (объект disnake.Embed)
        if isinstance(embed_or_str, disnake.Embed):
            await message.channel.send(embed=embed_or_str)
        elif isinstance(embed_or_str, str):
            await message.channel.send(embed=disnake.Embed(description=embed_or_str))  # Отправка строки как обычного сообщения
        else:
            await message.channel.send("Не удалось получить информацию о PR или Issue.")


async def check_time_transfer_with_fuzz(message):
    """
    Проверяет наличие фраз, связанных с переносом времени, используя fuzz.
    """
    time_transfer_phrases = [
        "а где перенос времени",
        "где перенести время",
        "как перевести время",
        "перенос времени на роли",
        "перенос времени",
        "перенос времени с проекта",
        "Тут есть перенос времени",
        "я хочу понять где перенести время на этом проекте",
        "я хочу понять где перенести время",
        "хочу понять где перенести время",
    ]

    # Проходим по каждой фразе и проверяем на совпадения с помощью fuzz
    for phrase in time_transfer_phrases:
        if fuzz.token_sort_ratio(message.content.lower(), phrase) > 80:
            # Ответ бота
            response = (
                "Вы говорите о переносе времени? Для таких вопросов ты можешь обратиться в следующий канал: "
                "https://discord.com/channels/901772674865455115/1172159356117200936"
            )
            
            # Отправляем ответ в канал
            await message.channel.send(response)
            break

async def isinstance_chat(message):
    try:
        # Если сообщение пришло в личные сообщения
        if isinstance(message.channel, disnake.DMChannel):
            # Если это не команда (не начинается с префикса)
            if not message.content.startswith(bot.command_prefix):
                # Отправляем ответ на сообщение
                await message.channel.send(
                    "Здравствуйте! Спасибо за ваше сообщение. "
                    "Ваше предложение или баг-репорт отправлен техническому администратору. "
                    "Мы будем стараться улучшать сервис и благодарны за ваш вклад! 😊"
                )
                
                # ID канала, куда нужно отправить сообщение
                target_channel_id = 1333381720996843551  # Замените на нужный канал
                # Получаем канал по ID
                target_channel = bot.get_channel(target_channel_id)
                if target_channel:
                    embed = disnake.Embed(
                        title="Новый отзыв/баг-репорт",
                        description=f"Сообщение от пользователя {message.author.display_name} ({message.author.mention}) ({message.author.id}):",
                        color=disnake.Color.yellow()
                    )
                    embed.add_field(
                        name="Текст сообщения:",
                        value=message.content,
                        inline=False
                    )
                    embed.set_footer(
                        text=f"Отправлено: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')} от {message.author.display_name}",
                        icon_url=message.author.avatar.url
                    )
                    embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
                    )
                    # Пересылаем сообщение в целевой канал
                    await target_channel.send(embed=embed)
                else:
                    print(f"Не удалось найти канал с ID {target_channel_id}")
        return
    except Exception as e:
        # Логирование ошибки (можно заменить на логгер)
        print(f"Ошибка при обработке сообщения в личных сообщениях: {e}")
        # Можно отправить пользователю сообщение об ошибке
        try:
            await message.channel.send(
                "Извините, произошла ошибка при обработке "
                "вашего сообщения. Пожалуйста, попробуйте позже."
            )
        except Exception as inner_error:
            print(f"Ошибка при отправке сообщения об ошибке: {inner_error}")
