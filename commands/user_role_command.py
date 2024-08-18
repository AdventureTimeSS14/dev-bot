import discord

from bot_init import bot


@bot.command()
async def user_role(ctx, *role_names: str):
    """Команда для получения списка пользователей с заданной ролью по имени."""

    role_name = " ".join(role_names)
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send(f"Роль '{role_name}' не найдена.")
        return

    members_with_role = [member.name for member in role.members]

    if members_with_role:
        await ctx.send(f'Пользователи с ролью {role.name}: {", ".join(members_with_role)}')
    else:
        await ctx.send(f'Нет пользователей с ролью {role.name}.')
