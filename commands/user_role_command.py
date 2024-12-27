"""
Модуль команды для получения все никнеймов относящихся к введённой роли.
"""

import discord

from bot_init import bot


@bot.command()
async def user_role(ctx, *role_names: str):
    """
    Команда для получения списка пользователей с заданной ролью по имени.
    """
    # Формируем имя роли из переданных аргументов
    role_name = " ".join(role_names).strip()

    if not role_name:
        await ctx.send(
            "❌ Вы не указали название роли. Используйте команду так: `&user_role <название роли>`."
        )
        return

    # Ищем роль в списке ролей сервера
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"❌ Роль '{role_name}' не найдена на сервере.")
        return

    # Получаем список пользователей с этой ролью
    members_with_role = [member.mention for member in role.members]

    if members_with_role:
        # Формируем сообщение с упоминанием пользователей
        members_list = ", ".join(members_with_role)
        await ctx.send(f"✅ Пользователи с ролью **{role.name}**:\n{members_list}")
    else:
        await ctx.send(f"⚠️ Нет пользователей с ролью **{role.name}**.")
