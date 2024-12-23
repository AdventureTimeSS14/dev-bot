import discord
from discord.ext import commands
from discord.utils import get

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import HEAD_ADT_TEAM


@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def remove_role(ctx, user: discord.Member, *role_names: str):
    """
    Команда для снятия указанных ролей у пользователя.
    """
    if not role_names:
        await ctx.send("Вы не указали роли для снятия. Используйте команду следующим образом: `&remove_role @User Role1 Role2`")
        return

    removed_roles = []
    errors = []

    for role_name in role_names:
        # Ищем роль по имени
        role = get(ctx.guild.roles, name=role_name)

        if role is None:
            errors.append(f"Роль '{role_name}' не найдена на сервере.")
            continue

        if role in user.roles:
            try:
                await user.remove_roles(role)
                removed_roles.append(role.name)
            except Exception as e:
                errors.append(f"Ошибка при снятии роли '{role.name}': {str(e)}")
        else:
            errors.append(f"У {user.name} нет роли '{role.name}'.")

    # Отправляем сообщение об успешных действиях
    if removed_roles:
        await ctx.send(f"Роли успешно сняты у {user.name}: {', '.join(removed_roles)}")

    # Отправляем сообщение об ошибках
    if errors:
        await ctx.send("Возникли следующие ошибки:\n" + "\n".join(errors))
