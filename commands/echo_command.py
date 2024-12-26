"""
Этот модуль содержит команду 'echo', которая повторяет переданное сообщение,
если пользователь является владельцем бота.
"""

import discord

from bot_init import bot
from config import MY_USER_ID


@bot.command(name="echo", help="Повторяет переданное сообщение. Доступна только для владельца бота.")
async def echo(ctx, *, message: str):
    """
    Команда для повторения сообщения.
    Доступ к команде ограничен пользователем с ID из MY_USER_ID.
    """
    # Проверка прав доступа
    if ctx.author.id != MY_USER_ID:
        await ctx.reply("❌ У вас нет доступа к этой команде.", mention_author=False)
        return

    try:
        # Удаление исходного сообщения
        await ctx.message.delete()

        # Отправка повторённого сообщения
        await ctx.send(message)

    except discord.Forbidden:
        # Если бот не имеет прав на удаление сообщений
        await ctx.reply("⚠️ У меня нет прав для удаления сообщений.", mention_author=False)
    except discord.DiscordException as e:
        # Логирование других ошибок, связанных с Discord
        print(f"❌ Произошла ошибка в команде 'echo': {e}")
        await ctx.reply("❌ Произошла ошибка при выполнении команды. Проверьте логи.", mention_author=False)
