import discord

from bot_init import bot
from data import JsonData

data = JsonData()

@bot.command(name='help')
async def help_command(ctx):
    help_command = data.get_data('help_command')
    
    embed = discord.Embed(
        title=help_command["title"],
        color=discord.Color.dark_green()
    )
    embed.add_field(
        name=help_command["name_1"],
        value=help_command["context_1"],
        inline=False
    )
    embed.add_field(
        name=help_command["name_2"],
        value=help_command["context_2"],
        inline=False
    )
    embed.add_field(
        name=help_command["name_3"],
        value=help_command["context_3"],
        inline=False
    )
    embed.add_field(
        name=help_command["name_4"],
        value=help_command["context_4"],
        inline=False
    )
    embed.add_field(
        name=help_command["name_5"],
        value=help_command["context_5"],
        inline=False
    )
    embed.set_author(
        name=ctx.author.name, 
        icon_url=ctx.author.avatar.url
    )

    await ctx.send(embed=embed)
    