import discord

from bot_init import bot
from config import ADMIN_TEAM


@bot.command()
async def team_help(ctx):
    """
    Команда для вывода справки по управлению отделом.
    """
    # Получение канала для логирования действий
    channel_get = bot.get_channel(ADMIN_TEAM)

    if not channel_get:
        await ctx.send("Не удалось найти канал для логирования действий.")
        return

    # Создание Embed сообщения
    embed = discord.Embed(
        title="📚 Команды для управления сотрудниками отдела",
        description="📃 Основные команды для управления отделом и должностями:",
        color=discord.Color.gold()
    )

    # Основные команды
    embed.add_field(
        name="&new_team",
        value=(
            "`&new_team <пользователь> <роль отдела> <роль должности>`\n"
            f"Пример: `&new_team @User Администрация \"Главный Администратор\"`\n"
            f"Добавляет сотрудника в отдел и отправляет сообщение в {channel_get.mention}."
        ),
        inline=False
    )
    embed.add_field(
        name="&remove_team",
        value=(
            "`&remove_team <пользователь> <роль отдела> <роль должности> <причина>`\n"
            f"Пример: `&remove_team @User Администрация \"Главный Администратор\" \"Причина\"`\n"
            f"Удаляет сотрудника из отдела и отправляет сообщение в {channel_get.mention}."
        ),
        inline=False
    )
    embed.add_field(
        name="&add_vacation",
        value=(
            "`&add_vacation <пользователь> <срок DD.MM.YYYY> <причина>`\n"
            f"Пример: `&add_vacation @User 22.02.2024 \"Отпуск\"`\n"
            f"Выдает роль отпуска пользователю и отправляет сообщение в {channel_get.mention}."
        ),
        inline=False
    )
    embed.add_field(
        name="&end_vacation",
        value=(
            "`&end_vacation <пользователь>`\n"
            f"Пример: `&end_vacation @User`\n"
            f"Удаляет роль отпуска и отправляет сообщение в {channel_get.mention}."
        ),
        inline=False
    )
    embed.add_field(
        name="&tweak_team",
        value=(
            "`&tweak_team <пользователь> <старая роль> <новая роль> <причина>`\n"
            f"Пример: `&tweak_team @User \"Старшая роль\" \"Новая роль\" \"Причина\"`\n"
            f"Изменяет роль сотрудника и отправляет сообщение в {channel_get.mention}."
        ),
        inline=False
    )

    # Дополнительные команды
    embed.add_field(
        name="🚨 Дополнительные команды:",
        value="Список команд, которые не отправляют сообщения в лог-канал:",
        inline=False
    )
    embed.add_field(
        name="&add_role",
        value=(
            "`&add_role <пользователь> <роль/роли>`\n"
            f"Пример: `&add_role @User Отпускник Хост Разработчик`\n"
            f"Добавляет неограниченное количество ролей пользователю."
        ),
        inline=False
    )
    embed.add_field(
        name="&remove_role",
        value=(
            "`&remove_role <пользователь> <роль/роли>`\n"
            f"Пример: `&remove_role @User Отпускник Хост Разработчик`\n"
            f"Удаляет неограниченное количество ролей у пользователя."
        ),
        inline=False
    )

    # Дополнительные указания
    embed.add_field(
        name="ℹ️ Примечания:",
        value=(
            "1. При написании ролей из нескольких слов используйте двойные кавычки.\n"
            "2. Можно использовать пинг, ID или имя пользователя/роли."
        ),
        inline=False
    )

    # Информация об отправителе команды
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

    # Отправляем Embed
    await ctx.send(embed=embed)
