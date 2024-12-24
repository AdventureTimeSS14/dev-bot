import discord

from bot_init import bot
from config import ADMIN_TEAM

commands_info = {
    "Основные команды": {
        "&new_team": {
            "description": "Добавляет сотрудника в отдел и отправляет сообщение в 🌀админ-состав.",
            "example": '&new_team @User Администрация "Главный Администратор"',
            "syntax": "&new_team <пользователь> <роль отдела> <роль должности>"
        },
        "&remove_team": {
            "description": "Удаляет сотрудника из отдела и отправляет сообщение в 🌀админ-состав.",
            "example": '&remove_team @User Администрация "Главный Администратор" "Причина"',
            "syntax": "&remove_team <пользователь> <роль отдела> <роль должности> <причина>"
        },
        "&tweak_team": {
            "description": "Изменяет роль сотрудника и отправляет сообщение в 🌀админ-состав.",
            "example": '&tweak_team @User "Старшая роль" "Новая роль" "Причина"',
            "syntax": "&tweak_team <пользователь> <старая роль> <новая роль> <причина>"
        },
        "&add_vacation": {
            "description": "Выдает роль отпуска пользователю и отправляет сообщение в 🌀админ-состав.",
            "example": '&add_vacation @User 22.02.2024 "Отпуск"',
            "syntax": "&add_vacation <пользователь> <срок DD.MM.YYYY> <причина>"
        },
        "&end_vacation": {
            "description": "Удаляет роль отпуска и отправляет сообщение в 🌀админ-состав.",
            "example": '&end_vacation @User',
            "syntax": "&end_vacation <пользователь>"
        },
        "&extend_vacation": {  # Новая команда для продления отпуска
            "description": "Продлевает срок отпуска пользователю, обновляя дату окончания отпуска и причину.",
            "example": '&extend_vacation @User 30.12.2024 "Необходимость дополнительных выходных"',
            "syntax": "&extend_vacation <пользователь> <новый срок DD.MM.YYYY> <причина>"
        }
    },
    "Дополнительные команды": {
        "&add_role": {
            "description": "Добавляет неограниченное количество ролей пользователю.",
            "example": '&add_role @User Отпускник Хост Разработчик',
            "syntax": "&add_role <пользователь> <роль/роли>"
        },
        "&remove_role": {
            "description": "Удаляет неограниченное количество ролей у пользователя.",
            "example": '&remove_role @User Отпускник Хост Разработчик',
            "syntax": "&remove_role <пользователь> <роль/роли>"
        }
    },
    "Примечания": [
        "1. При написании ролей из нескольких слов используйте двойные кавычки.",
        "2. Можно использовать пинг, ID или имя пользователя/роли."
    ]
}

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

    # Формирование описания для Embed сообщения
    embed_description = "📃 **Основные команды для управления отделом и должностями:**\n"
    
    # Добавляем команды из словаря
    for category, commands in commands_info.items():
        if isinstance(commands, dict):
            embed_description += f"\n**{category}:**\n"
            for command, details in commands.items():
                embed_description += (f"\n**{command}**:\n"
                                      f"  - Синтаксис: `{details['syntax']}`\n"
                                      f"  - Пример: `{details['example']}`\n"
                                      f"  - Описание: {details['description']}\n")
        elif isinstance(commands, list):
            embed_description += f"\n**{category}:**\n"
            for note in commands:
                embed_description += f"- {note}\n"

    # Создание Embed сообщения
    embed = discord.Embed(
        title="📚 Команды для управления сотрудниками отдела",
        description=embed_description,
        color=discord.Color.gold()
    )

    # Информация об отправителе команды
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

    # Отправляем Embed
    await ctx.send(embed=embed)
