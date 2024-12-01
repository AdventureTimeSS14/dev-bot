import discord

from bot_init import bot
from config import ADMIN_TEAM


@bot.command()
async def team_help(ctx):
    # Получение ID канала
    channel = ADMIN_TEAM
    channel_get = bot.get_channel(channel)

    embed = discord.Embed(
        title="📚 Команды для управления сотрудниками отдела",
        description="📃 Список основных команд:",
        color=discord.Color.gold()
    )
    embed.add_field(
        name="&new_team <пользователь>  <роль отдела>  <роль должности>", 
        value=f"```Принимает пользователя в отдел на определенную должность и отправляет сообщение в {channel_get}\nПример: &new_team @Darkiich Администрация \"Главный Администратор\"```", 
        inline=False)
    embed.add_field(
        name="&remove_team <пользователь>  <роль отдела>  <роль должности>", 
        value=f"```Увольняет пользователя из отдела и отправляет сообщение в {channel_get}.\nПример: &remove_team @Darkiich Администрация \"Главный Администратор\"```", 
        inline=False
    )
    embed.add_field(
        name="&add_vacation <пользователь>  <срок DD.MM.YYYY>  <причина>", 
        value=f"```Выдает пользователю роль отпуска и отправляет сообщение в {channel_get}.\nПример: &add_vacation @Darkiich 22.02.2024 \"Хочет отдыхать\"```", 
        inline=False
    )
    embed.add_field(
        name="&end_vacation <пользователь>", 
        value=f"```Закрывает и убирает роль отпуска у пользователя и отправляет сообщение в {channel_get}.\nПример: &end_vacation @Darkiich```", 
        inline=False
    )
    embed.add_field(
        name="&tweak_team <пользователь>  <старая роль>  <новая роль>  <причина>", 
        value=f"```Повышает/понижает пользователя в должности и отправляет сообщение в {channel_get}.\nПример: &tweak_role @Darkiich \"Главный Администратор\" \"Администратор\" \"Хороший\" ```", 
        inline=False
    )
    embed.add_field(
        name="", 
        value="🚨 Список дополнительных команд:", 
        inline=False
    )
    embed.add_field(
        name="&add_role <пользователь>  <роль/роли>", 
        value=f"```Добавляет неограниченное кол-во ролей и не отправляет сообщение в {channel_get}.\nПример: &add_role @Darkiich Отпускник Разработка Хост и.т.д```", 
        inline=False
    )
    embed.add_field(
        name="&remove_role <пользователь>  <роль/роли>", 
        value=f"```Забирает неограниченное кол-во ролей и не отправляет сообщение в {channel_get}.\nПример: &remove_role @Darkiich Отпускник Разработка Хост и.т.д```", 
        inline=False
    )
    embed.add_field(
        name="P.S. При написании ролей из двух и более слов используйте двойные кавычки. Также следует поступать и с причинами. Помните, что можно вписывать пинг, ID или никнейм пользователя, а также имя, ID или пинг роли.", 
        value="", 
        inline=True
    )
    embed.set_author(
        name=ctx.author.name, 
        icon_url=ctx.author.avatar.url
    )
    await ctx.send(embed=embed)