import discord
from discord.ext import commands
from discord.utils import get

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import HEAD_ADT_TEAM


@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def add_role(ctx, user: discord.Member, *role_names: str):
    """
    Добавляет одну или несколько ролей указанному пользователю.
    """
    if not role_names:
        await ctx.send("Пожалуйста, укажите хотя бы одну роль для добавления.")
        return

    # Переменная для подсчета успешно добавленных ролей
    added_roles = []

    for role_name in role_names:
        # Ищем роль по имени
        role = get(ctx.guild.roles, name=role_name)

        if not role:
            await ctx.send(f"❌ Роль '{role_name}' не найдена на сервере.")
            continue

        if role in user.roles:
            await ctx.send(f"ℹ️ {user.mention} уже имеет роль '{role.name}'.")
            continue

        try:
            # Добавляем роль пользователю
            await user.add_roles(role)
            added_roles.append(role.name)
        except discord.Forbidden:
            await ctx.send(f"❌ У меня недостаточно прав для добавления роли '{role.name}' пользователю {user.mention}.")
        except discord.HTTPException as e:
            print(f"Ошибка при добавлении роли '{role.name}': {e}")
            await ctx.send(f"❌ Не удалось добавить роль '{role.name}' для {user.mention} из-за ошибки.")

    # Если добавлены роли, выводим итоговое сообщение
    if added_roles:
        roles_list = ", ".join(added_roles)
        await ctx.send(f"✅ Роли ({roles_list}) успешно добавлены для {user.mention}.")

    # Если не удалось добавить ни одной роли
    if not added_roles and role_names:
        await ctx.send(f"❌ Не удалось добавить ни одной роли для {user.mention}. Проверьте права и правильность ввода ролей.")
