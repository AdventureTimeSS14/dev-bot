import discord
from discord.ext import commands
from discord.utils import get

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import HEAD_ADT_TEAM


@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def add_role(ctx, user: discord.Member, *role_names: str):
    # Получаем список всех ролей на сервере
    guild_roles = ctx.guild.roles

    for role_name in role_names:
        # Ищем роль по имени
        role = get(guild_roles, name=role_name)

        if role is None:
            await ctx.send(f"Роль '{role_name}' не найдена на сервере.")
            continue  # Переходим к следующей роли

        if role in user.roles:
            await ctx.send(f"{user.name} уже имеет роль '{role.name}'.")
        else:
            try:
                await user.add_roles(role)
                await ctx.send(f"Роль '{role.name}' успешно добавлена для {user.name}.")
            except discord.Forbidden:
                await ctx.send(f"У меня нет прав для добавления роли '{role.name}' пользователю {user.name}.")
            except discord.HTTPException as e:
                print("Возникла ошибка при добавлении роли:", e)
                await ctx.send(f"Не удалось добавить роль '{role.name}' для {user.name} из-за ошибки.")