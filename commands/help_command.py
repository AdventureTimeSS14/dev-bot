"""
Модуль вызова помощи и подсказок
"""

import disnake

from bot_init import bot
from components.button_help_components import action_row_button_help


@bot.command(name="help")
async def help_command(ctx):
    """
    Просто вызвается пользователем &help
    И отправляет embed
    """
    # Данные для команды help
    # pylint: disable=C0301
    help_command_text = {
        "title": "📚 Помощь по командам",
        "name_1": "Основные команды:",
        "context_1": (
            "❓ &help - Показать это сообщение.\n"
            "💾 &db_help - Помощь по управлению MariaDB.\n"
            "👥 &team_help - Выводит помощь по командам для руководства.\n"
            "⚙️ &admin_help - Помощь по командам для управления сервером.\n"
            "🛠  &git_help - Помощь по командам связанных с GitHub\n"
            "🏓 &ping - Выводит задержку ответа.\n"
            "🔄 &echo <сообщение> - Повторить ваше сообщение.\n"
            '🎭 &user_role "<роль>" - Показать список пользователей с указанной ролью.\n'
            "🤖 &gpt <промт> - ChatGPT 3.5 turbo.\n"
            "🖥️ &status - Выводит информацию о текущем статусе МРП сервера, количестве игроков и раунде.\n"
            "⏳ &uptime - Показывает время работы бота и его статус.\n"
        ),
        "name_2": "Доп. возможности:",
        "context_2": (
            "🤗 Обнимает в ответ.\n"
            "🧰 Отправляет чейнжлоги в специальный канал.\n"
            "🕴 Обновляет список сотрудников команды Adventure Time в специальном канале.\n"
            "🖥️ Обновляет статус сервера и время работы бота в специальном канале.\n"
            "🔎 Ищет в текстах сообщений отправленных пользователями [n13] [] и выводит ссылку на пулл реквест, \n"
            "если n - new новый репозиторий o - old старый репозиторий.\n"
            "\nПримеры:\n..[n213]..\n..[o3]..\n"
        ),
        "name_3": "Доп. информация:",
        "context_3": "✨ Если у вас есть вопросы или вам нужна помощь, обращайтесь к создателю: Schrödinger's Cutie🖤👾",
        "name_4": "Разработчики:",
        "context_4": "👨‍💻 Автор: Schrodinger71\n🛠️ Maintainer: Schrodinger71\n🤝 Contributors: nixsilvam, xelasto, mskaktus\n📡 Хост: 🐈‍⬛github-actions[bot]",
        "name_5": "Репозиторий бота:",
        "context_5": "🔗 GitHub: https://github.com/AdventureTimeSS14/Dev-bot",
    }

    # Создаем embed-сообщение
    embed = disnake.Embed(
        title=help_command_text["title"], color=disnake.Color.dark_green()
    )
    embed.add_field(
        name=help_command_text["name_1"],
        value=help_command_text["context_1"],
        inline=False,
    )
    embed.add_field(
        name=help_command_text["name_2"],
        value=help_command_text["context_2"],
        inline=False,
    )
    embed.add_field(
        name=help_command_text["name_3"],
        value=help_command_text["context_3"],
        inline=False,
    )
    embed.add_field(
        name=help_command_text["name_4"],
        value=help_command_text["context_4"],
        inline=False,
    )
    embed.add_field(
        name=help_command_text["name_5"],
        value=help_command_text["context_5"],
        inline=False,
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

    # Отправляем embed-сообщение
    await ctx.send(embed=embed, components=[action_row_button_help])
