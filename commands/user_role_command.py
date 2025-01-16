"""
Модуль команды для получения все никнеймов относящихся к введённой роли.
"""

import disnake

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
            "❌ **Вы не указали название роли.**\n"
            "Используйте команду так: `&user_role <название роли>`."
        )
        return

    # Ищем роль в списке ролей сервера
    role = disnake.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"❌ **Роль '{role_name}' не найдена на сервере.**")
        return

    # Получаем список пользователей с этой ролью
    members_with_role = [member.name for member in role.members]

    if members_with_role:
        # Формируем сообщение с подсчётом пользователей
        members_count = len(members_with_role)
        members_list = "\n".join([f"👤 **{member}**" for member in members_with_role])
        await ctx.send(
            f"✅ **Пользователи с ролью '{role.name}':** ({members_count})\n\n"
            f"{members_list}"
        )
    else:
        await ctx.send(f"⚠️ **Нет пользователей с ролью '{role.name}'.**")
