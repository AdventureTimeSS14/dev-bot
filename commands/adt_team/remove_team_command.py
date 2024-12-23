import discord
from discord.ext import commands

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import ADMIN_TEAM, HEAD_ADT_TEAM


@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def remove_team(ctx, user: discord.Member, role_dep: discord.Role, role_job: discord.Role, *, reason: str):
    """
    Команда для снятия сотрудника с должности.
    """
    # Проверяем, существует ли канал для логирования
    channel_get = bot.get_channel(ADMIN_TEAM)
    if not channel_get:
        await ctx.send("Не удалось найти канал для логирования действий.")
        return

    removed_roles = []
    errors = []

    # Проверяем и удаляем роли у пользователя
    for role in [role_dep, role_job]:
        if role in user.roles:
            try:
                await user.remove_roles(role)
                removed_roles.append(role)
            except Exception as e:
                errors.append(f"Ошибка при удалении роли **{role.name}**: {str(e)}")
        else:
            errors.append(f"У {user.name} нет роли **{role.name}**.")

    # Обрабатываем результаты
    if removed_roles:
        role_names = ", ".join([role.name for role in removed_roles])
        await ctx.send(f"Роли успешно сняты: {role_names}")
    if errors:
        for error in errors:
            await ctx.send(error)

    # Если обе роли успешно удалены, отправляем Embed в лог-канал
    if len(removed_roles) == 2:
        embed = discord.Embed(
            title="Снятие с должности",
            description=f"{ctx.author.mention} снял с должности {user.mention}.",
            color=role_job.color,
        )
        embed.add_field(name="Отдел:", value=f"**{role_dep.name}**", inline=False)
        embed.add_field(name="Должность:", value=f"**{role_job.name}**", inline=False)
        embed.add_field(name="Причина:", value=f"**{reason}**", inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        await channel_get.send(embed=embed)
    else:
        await ctx.send("Не удалось снять все указанные роли.")
