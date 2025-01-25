import disnake
import requests
from bot_init import bot
from config import AUTHOR, ACTION_GITHUB
from disnake.ext import commands

# Функция для получения списка участников организации на GitHub
def get_github_org_members():
    """Получает список участников организации на GitHub."""
    url = f'https://api.github.com/orgs/{AUTHOR}/members'
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на успешность запроса
        members = response.json()   # Получаем JSON-ответ с участниками
        return [member['login'] for member in members]  # Возвращаем список логинов участников
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении участников: {e}")
        return []

@bot.command(
    name="git_team",
    help="Выводит список участников организации на GitHub."
)
async def git_team(ctx):
    """
    Команда для вывода списка участников организации на GitHub.
    """
    members = get_github_org_members()

    if not members:
        await ctx.send("❌ Не удалось получить список участников организации.")
        return

    # Формируем строку с участниками
    members_list = "👤 **" + "**\n👤 ".join([f"**{member}**" for member in members])
    if len(members_list) > 2000:
        # Если список слишком длинный, выводим только первые 2000 символов
        members_list = members_list[:2000] + "..."
    
    # Создаём Embed с улучшенным дизайном
    embed = disnake.Embed(
        title="🌟 Список участников организации на GitHub 🚀",
        description=f"**Организация**: {AUTHOR}\n**Участники**:\n{members_list}",
        color=disnake.Color.dark_grey(),
        timestamp=disnake.utils.utcnow()
    )

    embed.set_footer(text=f"Запрос от {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    
    # Дополнительные поля для улучшения
    embed.add_field(
        name="👥 Кто может присоединиться?",
        value="**Только участники команды разработки** могут быть в списке участников. Если вы хотите присоединиться, пишите в https://discord.com/channels/901772674865455115/1297176881732386847.",
        inline=False
    )
    embed.add_field(
        name="📣 Внимание!",
        value="Это список всех участников организации на GitHub. Если вы хотите узнать больше информации о конкретном участнике, используйте команду &git_logininfo <login> для получения деталей о пользователе.",
        inline=False
    )

    # Отправляем Embed в канал
    await ctx.send(embed=embed)
