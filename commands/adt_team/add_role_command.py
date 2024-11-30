import discord

from bot_init import bot

@bot.command()
async def add_role(ctx, user: discord.Member, *roles: discord.Role):

    for role in roles:
        if role in user.roles:
            await ctx.send(f"{user.name} уже имеет роль {role.name}")
        else:
            try:
                await user.add_roles(role)
                await ctx.send(f"Роль **{role}** успешно добавлена для {user.name}.")
            except discord.Forbidden:
                await ctx.send("Недостаточно прав для добавления роли.")
            except discord.HTTPException:
                await ctx.send("Не удалось добавить роль.")