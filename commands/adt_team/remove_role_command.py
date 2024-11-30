import discord

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import HEAD_ADT_TEAM

@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def remove_role(ctx, user: discord.Member, *roles: discord.Role):

    for role in roles:
        if role in user.roles:
            try:
                await user.remove_roles(role)
                await ctx.send(f"Роль **{role}** успешно снята у {user.name}.")
            except discord.Forbidden:
                await ctx.send("Недостаточно прав для добавления роли.")
            except discord.HTTPException:
                await ctx.send("Не удалось добавить роль.")
        else:
            await ctx.send(f"У {user.name} нет роли {role.name}")