import discord

from bot_init import bot
from config import ADMIN_TEAM

@bot.command()
async def remove_team(ctx, user: discord.Member, *roles: discord.Role):
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

    for role in [role_dep, role_job]:
        if role in user.roles:
            try:
                await user.remove_roles(role)
                add_role.append(role)
                await ctx.send(f"Роль **{role}** успешно снята у {user.name}.")
            except discord.Forbidden:
                await ctx.send("Недостаточно прав для добавления роли.")
            except discord.HTTPException:
                await ctx.send("Не удалось добавить роль.")
        else:
            await ctx.send(f"У {user.name} нет такой роли {role.name}")

        # Отправляем сообщение в админ-состав
    if channel_get and len(add_role) == 2:
        embed = discord.Embed(
            title="Снятие с должности",
            description=f"{ctx.author.mention} снимает с должности {user.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name=f"Отдел: **{role_dep.name}**", value="", inline=False)
        embed.add_field(name=f"Должность: **{role_job.name}**", value="", inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await channel_get.send(embed=embed)