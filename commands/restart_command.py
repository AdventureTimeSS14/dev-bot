import sys

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from commands.misc.shutdows_deff import shutdown_def
from config import HEAD_ADT_TEAM, LOG_CHANNEL_ID


@bot.command(name="restart")
@has_any_role_by_id(HEAD_ADT_TEAM)
async def restart(ctx):
    """
    Команда для перезапуска бота.
    Доступна только для пользователей с ролью из HEAD_ADT_TEAM.
    """
    try:
        # Уведомляем пользователя в текущем канале
        await ctx.send("🔄 Запущен протокол перезапуска. Пожалуйста, подождите.")

        # Выполняем действия перед завершением работы
        await shutdown_def()

        await ctx.send(
            f"⚠️ {bot.user} завершает свою работу! Перезапуск начнётся в течение 10 минут."
        )

        # Закрываем соединение бота
        await bot.close()

        # Завершаем процесс
        sys.exit(0)

    except Exception as e:
        # Обработка ошибок
        print(f"❌ Произошла ошибка при попытке перезапуска: {e}")
        await ctx.send("❌ Произошла ошибка при попытке перезапуска. Проверьте логи.")