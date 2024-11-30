import discord

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import ADMIN_TEAM, HEAD_ADT_TEAM


@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def tweak_team(ctx, user: discord.Member, old_role: discord.Role, new_role: discord.Role):

    # Получение ID канала
    channel = ADMIN_TEAM
    channel_get = bot.get_channel(channel)

    if channel_get:
        if old_role in user.roles:
            try:
                await user.remove_roles(old_role)
                await user.add_roles(new_role)
                await ctx.send(f"Роль **{old_role.name}** была заменена на **{new_role.name}** у {user.name}.")

                if old_role < new_role:
                    embed_promotion = discord.Embed(
                        title="Повышение в должности",
                        description=f"{ctx.author.mention} повышает {user.mention}.",
                        color=discord.Color.green()
                    )
                    embed_promotion.add_field(name=f"Старая должность: **{old_role.name}**", value="", inline=False)
                    embed_promotion.add_field(name=f"Новая должность: **{new_role.name}**", value="", inline=False)
                    embed_promotion.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await channel_get.send(embed=embed_promotion)

                elif old_role > new_role:
                    embed_promotion = discord.Embed(
                        title="Понижение в должности",
                        description=f"{ctx.author.mention} понижает {user.mention}.",
                        color=discord.Color.green()
                    )
                    embed_promotion.add_field(name=f"Старая должность: **{old_role.name}**", value="", inline=False)
                    embed_promotion.add_field(name=f"Новая должность: **{new_role.name}**", value="", inline=False)
                    embed_promotion.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await channel_get.send(embed=embed_promotion)

            except discord.Forbidden:
                await ctx.send("Недостаточно прав для добавления роли.")
            except discord.HTTPException:
                await ctx.send("Не удалось добавить роль.")
        else:
            await ctx.send(f"У {user.name} нет роли **{old_role.name}**")