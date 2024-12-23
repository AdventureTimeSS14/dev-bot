import sys
from bot_init import bot
from commands.misc.shutdows_deff import shutdown_def
from commands.misc.check_roles import has_any_role_by_id
from config import HEAD_ADT_TEAM

@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def restart(ctx):
    """
    Команда для перезапуска бота.
    """
    await ctx.send(f'Запущен протокол перезапуска.')
    await shutdown_def()
    await bot.close()
    sys.exit(0)
    