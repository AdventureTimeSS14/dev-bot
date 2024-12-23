import sys

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from commands.misc.shutdows_deff import shutdown_def
from config import HEAD_ADT_TEAM, LOG_CHANNEL_ID


@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def restart(ctx):
    """
    Команда для перезапуска бота.
    """
    await ctx.send(f'Запущен протокол перезапуска.')
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(f"{bot.user} завершает свою работу! Ожидайте перезапуска в течении 10 минут.")
    await shutdown_def()
    await bot.close()
    sys.exit(0)
    