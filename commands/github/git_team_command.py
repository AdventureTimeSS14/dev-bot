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

# Функция для получения списка владельцев (admins) из команд
def get_github_org_owners():
    """Получает список владельцев организации (admins) из команды."""
    url = f'https://api.github.com/orgs/{AUTHOR}/teams'

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        teams = response.json()
        return teams
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении команд: {e}")
        return []

# Функция для получения списка команд организации на GitHub
def get_github_teams():
    """Получает список команд организации на GitHub."""
    url = f'https://api.github.com/orgs/{AUTHOR}/teams'

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        teams = response.json()
        return teams
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении команд: {e}")
        return []

# Функция для получения участников команды
def get_team_members(team_slug):
    """Получает участников конкретной команды на GitHub."""
    url = f'https://api.github.com/orgs/{AUTHOR}/teams/{team_slug}/members'

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        members = response.json()
        return [member['login'] for member in members]
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении участников команды {team_slug}: {e}")
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
    teams = get_github_teams()

    if not members:
        await ctx.send("❌ Не удалось получить список участников организации.")
        return

    # Получение владельцев
    owners_slug = None
    mainteiners_slug = None

    # Поиск команд по slug
    for team in teams:
        if team['slug'] == 'owners':
            owners_slug = team['slug']
        elif team['slug'] == 'adt_maintainer':
            mainteiners_slug = team['slug']

    if not owners_slug:
        await ctx.send("❌ Не удалось найти команду владельцев (owners).")
        return

    if not mainteiners_slug:
        await ctx.send("❌ Не удалось найти команду мейнтейнеров (adt_mainteiner).")
        return

    # Получение участников команд
    owners = get_team_members(owners_slug)
    mainteiners = get_team_members(mainteiners_slug)

    # Сортировка участников
    sorted_owners = [member for member in members if member in owners]
    sorted_mainteiners = [member for member in members if member in mainteiners and member not in owners]
    sorted_members = [member for member in members if member not in owners and member not in mainteiners]

    # Формирование строк для embed
    owners_list = "👑 " + "\n👑 ".join([f"**{owner}**" for owner in sorted_owners])
    mainteiners_list = "🛠️ " + "\n🛠️ ".join([f"**{member}**" for member in sorted_mainteiners])
    members_list = "👤 " + "\n👤 ".join([f"**{member}**" for member in sorted_members])

    # Проверка длины сообщения
    combined_list = f"{owners_list}\n\n{mainteiners_list}\n\n{members_list}"
    if len(combined_list) > 2000:
        combined_list = combined_list[:2000] + "..."

    # Создание Embed
    embed = disnake.Embed(
        title="🌟 Список участников организации на GitHub 🚀",
        description=f"**Организация**: {AUTHOR}\n\n**Владельцы**:\n{owners_list}\n\n**Мейнтейнеры**:\n{mainteiners_list}\n\n**Остальные участники**:\n{members_list}",
        color=disnake.Color.dark_grey(),
        timestamp=disnake.utils.utcnow()
    )

    embed.set_footer(text=f"Запрос от {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

    # Отправляем Embed в канал
    await ctx.send(embed=embed)
