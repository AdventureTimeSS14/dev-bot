import discord
from discord.ext import commands
from discord.utils import get

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import HEAD_ADT_TEAM

@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def remove_role(ctx, user: discord.Member, *role_names: str):
    for role_name in role_names:
        # Ищем роль по имени
        role = get(ctx.guild.roles, name=role_name)

        if role is None:
            await ctx.send(f"Роль '{role_name}' не найдена на сервере.")
            continue  # Переходим к следующей роли

        if role in user.roles:
            try:
                await user.remove_roles(role)
                await ctx.send(f"Роль '{role.name}' успешно снята у {user.name}.")
            except Exception as e:
                print("Возникла ошибка при снятии роли:", e)
                await ctx.send(f"Не удалось снять роль '{role.name}' у {user.name}.")
        else:
            await ctx.send(f"У {user.name} нет роли '{role.name}'.")