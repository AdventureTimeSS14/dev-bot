import datetime

import disnake
from disnake.ext import commands
from disnake.ui import View
from components.button_help_components import button_bug_report

from bot_init import bot
from config import LOG_CHANNEL_ID


@bot.event
async def on_command(ctx):
    """
    Логирует выполнение команды в указанный лог-канал и выводит информацию в консоль.
    """
    # Получаем канал для логирования
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if not channel:
        print(f"❌ Лог-канал с ID {LOG_CHANNEL_ID} не найден.")
        return

    # Получаем текущее время
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Определяем, был ли вызов команды в ЛС или в канале сервера
    if isinstance(ctx.channel, disnake.DMChannel):
        channel_info = "ЛС с пользователем"
        # В ЛС не будет ссылки на сообщение с использованием guild
        message_link = f"https://discord.com/channels/@me/{ctx.channel.id}/{ctx.message.id}"
    else:
        channel_info = f"Канал {ctx.channel.name} в {ctx.guild.name}"
        message_link = (
            f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}"
        )

    # Формируем сообщение для логирования
    log_message = format_command_log_message(
        ctx, current_time, channel_info, message_link
    )

    # Отправляем лог-сообщение в канал
    try:
        await channel.send(log_message)
    except Exception as e:
        print(f"❌ Ошибка при отправке лог-сообщения в канал: {e}")

    # Логирование в консоль
    print(
        f"✅ Команда выполнена: {ctx.command.name} от {ctx.author} в {channel_info} в {current_time}"
    )


@bot.event
async def on_command_error(ctx, error):
    """
    Обрабатывает ошибки, связанные с выполнением команд.
    """
    view = View()
    view.add_item(button_bug_report)
    
    if isinstance(error, commands.CommandNotFound):

        
        # Если команда не найдена, отправляем сообщение с предложением использовать &help
        await ctx.send(
            "❌ Команда не найдена! "
            "Попробуйте использовать команду "
            "`&help`, чтобы узнать доступные команды.",
            view=view
        )
    else:
        # Если произошла другая ошибка, выводим её
        await ctx.send(f"❌ Произошла ошибка: {error}",
                       view=view
        )


def format_command_log_message(ctx, current_time, channel_info, message_link):
    """
    Форматирует сообщение для логирования информации о выполненной команде.

    :param ctx: Контекст команды.
    :param current_time: Время выполнения команды.
    :param channel_info: Информация о канале, в котором была выполнена команда.
    :param message_link: Ссылка на сообщение с командой.
    :return: Отформатированное сообщение для логирования.
    """
    return (
        f"🎯 **Команда выполнена:** `{ctx.command.name}`\n"
        f"🙋 **Пользователь:** {ctx.author} (ID: {ctx.author.id})\n"
        f"📄 **Канал:** {channel_info}\n"
        f"⏰ **Время:** {current_time}\n"
        f"🔗 **Ссылка на сообщение:** [Перейти к сообщению]({message_link})\n_ _"
    )
