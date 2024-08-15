import discord

from bot_init import bot


@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="📚 Помощь по командам",
        color=discord.Color.dark_green()
    )
    embed.add_field(
        name=
        value=
        inline=False
    )
    embed.add_field(
        name=
        value=
        inline=False
    )
    embed.add_field(
        name=
        value=
        inline=False
    )
    embed.add_field(
        name=
        value=
        inline=False
    )
    await ctx.send(embed=embed)