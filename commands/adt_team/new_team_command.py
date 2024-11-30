import discord

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import ADMIN_TEAM, HEAD_ADT_TEAM

@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def new_team(ctx, user: discord.Member, *roles: discord.Role):
    # Проверка на кол-во введеных ролей
    if len(roles) != 2:
        await ctx.send("Должно быть введенно две роли: <роль отдела> <роль должности>.")
        return

    # Получение ID канала
    channel = ADMIN_TEAM
    channel_get = bot.get_channel(channel)

    # Переменные для хранения двух вводимых ролей
    role_dep, role_job = roles

    # Массив для проверки введенных ролей
    add_role = []

    # Проверка на присутствие роли у пользователя
    for role in [role_dep, role_job]:
        if role in user.roles:
            await ctx.send(f"{user.name} уже имеет роль {role.name}")
        else:
            try:
                await user.add_roles(role)
                add_role.append(role)
                await ctx.send(f"Роль {role.name} успешно добавлена для {user.name}.")
            except discord.Forbidden:
                await ctx.send("Недостаточно прав для добавления роли.")
            except discord.HTTPException:
                await ctx.send("Не удалось добавить роль.")

    # Отправляем сообщение в админ-состав
    if channel_get and len(add_role) == 2:
        embed = discord.Embed(
            title="Назначение на должность",
            description=f"{ctx.author.mention} назначает {user.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name=f"Отдел: **{role_dep.name}**", value="", inline=False)
        embed.add_field(name=f"Должность: **{role_job.name}**", value="", inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await channel_get.send(embed=embed)