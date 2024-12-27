import traceback

from bot_init import bot
from config import LOG_CHANNEL_ID


@bot.event
async def on_error(event, *args, **kwargs):
    """
    Обрабатывает ошибки, произошедшие в событии.
    Логирует их в указанный канал и выводит в консоль для диагностики.
    """
    error_message = f"⚠️ Произошла ошибка в событии: `{event}`"

    # Получение трассировки ошибки
    error_traceback = traceback.format_exc()

    # Логирование ошибки в консоль
    print(error_message)
    print(error_traceback)

    # Логирование ошибки в указанный канал
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        try:
            await channel.send(
                f"{error_message}\n```{error_traceback[:1900]}```"
            )  # Урезаем до лимита Discord (2000 символов)
        except Exception as e:
            print(f"❌ Ошибка при отправке сообщения об ошибке в канал: {e}")
    else:
        print(f"❌ Канал с ID {LOG_CHANNEL_ID} не найден. Ошибка не записана в лог.")
