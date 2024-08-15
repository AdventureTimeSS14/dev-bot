from bot_init import bot
import discord

@bot.command()
async def user_role(ctx, *role_names: str):
    """Команда для получения списка пользователей с заданной ролью по имени."""

    # Объединяем все слова в строку, чтобы получить полное название роли
    role_name = " ".join(role_names)

    # Поиск роли по названию 
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    # Проверка, найдена ли роль
    if role is None:
        await ctx.send(f"Роль '{role_name}' не найдена.")
        return

    # Получение списка участников с этой ролью
    members_with_role = [member.name for member in role.members]

    # Вывод результата
    if members_with_role:
        await ctx.send(f'Пользователи с ролью {role.name}: {", ".join(members_with_role)}')
    else:
        await ctx.send(f'Нет пользователей с ролью {role.name}.')

# Словарь для хранения времени последнего использования команды для каждого пользователя
last_used = {}