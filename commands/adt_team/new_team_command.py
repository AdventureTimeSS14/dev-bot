import discord

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import ADMIN_TEAM, HEAD_ADT_TEAM


@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def new_team(ctx, user: discord.Member, *roles: discord.Role):
    """
    Команда для назначения пользователя на должность в команде.
    Требует две роли: <роль отдела> и <роль должности>.
    """
    if len(roles) != 2:
        await ctx.send("Ошибка: Укажите ровно две роли: <роль отдела> и <роль должности>.")
        return

    # Получаем роли
    role_department, role_position = roles
    assigned_roles = []
    errors = []

    # Проверяем и добавляем роли
    for role in [role_department, role_position]:
        if role in user.roles:
            errors.append(f"Роль **{role.name}** уже есть у {user.mention}.")
        else:
            try:
                await user.add_roles(role)
                assigned_roles.append(role.name)
            except Exception as e:
                errors.append(f"Ошибка при добавлении роли **{role.name}**: {str(e)}")

    # Отправляем сообщение о результатах
    if assigned_roles:
        await ctx.send(f"Роли успешно добавлены для {user.mention}: {', '.join(assigned_roles)}")
    if errors:
        await ctx.send("Возникли ошибки:\n" + "\n".join(errors))

    # Отправляем Embed в канал для уведомлений
    admin_channel = bot.get_channel(ADMIN_TEAM)
    if admin_channel and len(assigned_roles) == 2:
        embed = discord.Embed(
            title="Назначение на должность",
            description=f"{ctx.author.mention} назначает {user.mention}",
            color=role_position.color,
        )
        embed.add_field(name="Отдел", value=f"**{role_department.name}**", inline=False)
        embed.add_field(name="Должность", value=f"**{role_position.name}**", inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        await admin_channel.send(embed=embed)
