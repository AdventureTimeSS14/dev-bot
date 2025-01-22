import disnake
import time
from disnake.ext import commands

from bot_init import bot

# Класс для создания кнопок переключения помощи
class HelpButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        # Используем текущую метку времени для уникальности custom_id
        timestamp = str(int(time.time()))  # Получаем уникальный timestamp
        self.add_item(disnake.ui.Button(label="Основные команды", custom_id=f"help_main_commands_{timestamp}", style=disnake.ButtonStyle.green))
        self.add_item(disnake.ui.Button(label="Доп. возможности", custom_id=f"help_additional_features_{timestamp}", style=disnake.ButtonStyle.green))
        self.add_item(disnake.ui.Button(label="Информация", custom_id=f"help_information_{timestamp}", style=disnake.ButtonStyle.green))

    # Функции для обработки нажатий кнопок
    @disnake.ui.button(label="Основные команды", custom_id="help_main_commands", style=disnake.ButtonStyle.green)
    async def on_help_1(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="📚 Помощь по командам",
            description="❓ &help - Показать это сообщение.\n💾 &db_help - Помощь по управлению MariaDB.\n👥 &team_help - Выводит помощь по командам для руководства.\n⚙️ &team_help - Помощь по командам для управления сервером.\n🏓 &ping - Выводит задержку ответа.\n🔄 &echo <сообщение> - Повторить ваше сообщение.\n🎭 &user_role \"<роль>\" - Показать список пользователей с указанной ролью.\n🤖 &gpt <промт> - ChatGPT 3.5 turbo.\n🌳 &forks n/o - Вывести список форков AdventureTimeSS14/space_station_ADT или AdventureTimeSS14/space_station.\n👀 &review n/o - Вывести список пулл-реквестов для ревью (n - новый, o - старый репозиторий).\n📝 &achang n/o - Вывести список пулл-реквестов, ожидающих изменений в репозитории (n - новый, o - старый).\n🗓️ &milestones n/o - Выводит список всех майлстоунов (n - новый, o - старый репозиторий).\n🖥️ &status - Выводит информацию о текущем статусе МРП сервера, количестве игроков и раунде.\n⏳ &uptime - Показывает время работы бота и его статус."
        )
        await interaction.response.edit_message(embed=embed)

    @disnake.ui.button(label="Доп. возможности", custom_id="help_additional_features", style=disnake.ButtonStyle.green)
    async def on_help_2(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="Доп. возможности:",
            description="🤗 Обнимает в ответ.\n🧰 Отправляет чейнжлоги в специальный канал.\n🕴 Обновляет список сотрудников команды Adventure Time в специальном канале.\n🖥️ Обновляет статус сервера и время работы бота в специальном канале.\n🔎 Ищет в текстах сообщений отправленных пользователями [n13] [] и выводит ссылку на пулл реквест, если n - new новый репозиторий o - old старый репозиторий.\nПримеры:\n..[n213]..\n..[o3].."
        )
        await interaction.response.edit_message(embed=embed)

    @disnake.ui.button(label="Информация", custom_id="help_information", style=disnake.ButtonStyle.green)
    async def on_help_3(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="Информация и разработчики:",
            description="✨ Если у вас есть вопросы или вам нужна помощь, обращайтесь к создателю: Schrödinger's Cutie🖤👾\n\n👨‍💻 Автор: Schrodinger71\n🛠️ Maintainer: Schrodinger71\n🤝 Contributors: nixsilvam, xelasto, mskaktus\n📡 Хост: 🐈‍⬛github-actions[bot]\n\n🔗 GitHub: https://github.com/AdventureTimeSS14/Dev-bot"
        )
        await interaction.response.edit_message(embed=embed)


@bot.command(name="help")
async def help_command(ctx):
    """
    Просто вызывается пользователем &help и отправляет embed с кнопками для выбора разделов.
    """
    embed = disnake.Embed(
        title="📚 Помощь по командам",
        description="Выберите раздел помощи, нажав на одну из кнопок ниже:"
    )

    # Создаем объект с кнопками, уникальными custom_id
    view = HelpButtonView()

    # Отправляем embed-сообщение с кнопками
    await ctx.send(embed=embed, view=view)
