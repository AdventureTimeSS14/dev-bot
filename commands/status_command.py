from bot_init import bot
from config import SS14_ADDRESS
from events.update_status import (create_status_embed,
                                  get_ss14_server_status_second)


@bot.command(name="status")
async def get_status_command(ctx):
    """
    Команда для получения статуса сервера SS14 в чате Discord.
    """
    try:
        # Получаем данные статуса с сервера
        status_data = await get_ss14_server_status_second(SS14_ADDRESS)

        # Если данные не получены, уведомляем пользователя
        if not status_data:
            await ctx.send("❌ Ошибка при получении статуса с сервера.")
            return

        # Создаем Embed сообщение с использованием данных
        embed = create_status_embed(SS14_ADDRESS, status_data, ctx.author)
        await ctx.send(embed=embed)

    except Exception as e:
        # Обработка любых ошибок
        print(f"❌ Произошла ошибка в команде 'status': {e}")
        await ctx.send("❌ Произошла ошибка при выполнении команды. Повторите позже.")
