import discord

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import ADMIN_TEAM, VACATION_ROLE, HEAD_ADT_TEAM

@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def add_vacation(ctx, user: discord.Member):

    # ID роли отпуска
    role_vac = ctx.guild.get_role(VACATION_ROLE)

    # Получение ID канала
    channel = ADMIN_TEAM
    channel_get = bot.get_channel(channel)

    if role_vac in ctx.guild.roles:
        if role_vac in user.roles:
            await ctx.send(f"{user.name} уже имеет роль {role_vac.name}")
        else:
            try:
                # Добавляем роль указанному пользователю
                await user.add_roles(role_vac)
                await ctx.send(f"Роль {role_vac.name} была успешно добавлена {user.name}.")

                # Отправляем сообщение в админ-состав
                if channel_get:
                    embed = discord.Embed(
                        title="Выдача отпуска",
                        description=f"{ctx.author.mention} выдает отпуск {user.mention}. Хорошего отдыха!",
                        color=discord.Color.green()
                    )
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await channel_get.send(embed=embed)

            except discord.Forbidden:
                await ctx.send("У меня нет разрешения на изменение ролей этого пользователя.")
            except discord.HTTPException:
                await ctx.send(f"Не удалось добавить роль.")
    else:
        await ctx.send("Роль отпуска не найдена")