import discord

from bot_init import bot


@bot.command()
async def db_help(ctx):
    embed = discord.Embed(
        title="Команды для управления MariaDB",
        description="Список доступных команд для работы с базой данных:",
        color=discord.Color.dark_purple()
    )
    embed.add_field(name="&db_info", value="Выводит всю основную информацию о базе данных.", inline=False)
    embed.add_field(name="&db_status", value="Сообщает статус подключения к MariaDB.", inline=False)
    await ctx.send(embed=embed)