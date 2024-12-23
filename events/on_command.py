import datetime

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

    # Формируем сообщение для логирования
    log_message = format_command_log_message(ctx, current_time)

    # Отправляем лог-сообщение в канал
    try:
        await channel.send(log_message)
    except Exception as e:
        print(f"❌ Ошибка при отправке лог-сообщения в канал: {e}")

    # Логирование в консоль
    print(f"✅ Команда выполнена: {ctx.command.name} от {ctx.author} в канале {ctx.channel} в {current_time}")


def format_command_log_message(ctx, current_time):
    """
    Форматирует сообщение для логирования информации о выполненной команде.
    """
    return (
        f"**Команда выполнена:** `{ctx.command.name}`\n"
        f"**Пользователь:** {ctx.author} (ID: {ctx.author.id})\n"
        f"**Канал:** {ctx.channel} (ID: {ctx.channel.id})\n"
        f"**Время:** {current_time}\n"
        f"**Ссылка на сообщение:** [Перейти к сообщению]"
        f"(https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id})"
    )
