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

# Функция для получения владельцев репозитория на GitHub
def get_github_repo_owners():
    """Получает список владельцев репозитория на GitHub."""
    url = f'https://api.github.com/orgs/{AUTHOR}/memberships'
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        members = response.json()
        # Извлекаем владельцев (admins)
        owners = [member['login'] for member in members if member['role'] == 'admin']
        return owners
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении владельцев: {e}")
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
    owners = get_github_repo_owners()

    if not members:
        await ctx.send("❌ Не удалось получить список участников организации.")
        return

    # Получаем список команд и участников основной команды (Mainteiners)
    teams = get_github_teams()
    mainteiners_team_slug = None
    
    # Ищем команду с названием "Mainteiners"
    for team in teams:
        if team['name'].lower() == 'adt_maintainer':
            mainteiners_team_slug = team['slug']
            break

    if not mainteiners_team_slug:
        await ctx.send("❌ Не удалось найти команду.")
        return

    # Получаем участников основной команды
    mainteiners_members = get_team_members(mainteiners_team_slug)

    # Сортируем участников
    sorted_owners = [member for member in owners if member in members]
    sorted_mainteiners = [member for member in members if member in mainteiners_members]
    sorted_members = [member for member in members if member not in owners and member not in mainteiners_members]

    # Формируем строку с владельцами (с эмодзи короны)
    owners_list = "👑 " + "\n👑 ".join([f"**{owner}**" for owner in sorted_owners])
    
    # Формируем строку с участниками основной команды (Mainteiners)
    mainteiners_list = "🛠️ " + "\n🛠️ ".join([f"**{member}** (Mainteiner)" for member in sorted_mainteiners])
    
    # Формируем строку с остальными участниками
    members_list = "👤 " + "\n👤 ".join([f"**{member}**" for member in sorted_members])

    if len(owners_list + mainteiners_list + members_list) > 2000:
        # Если список слишком длинный, выводим только первые 2000 символов
        combined_list = owners_list + "\n\n" + mainteiners_list + "\n\n" + members_list
        combined_list = combined_list[:2000] + "..."
    else:
        combined_list = owners_list + "\n\n" + mainteiners_list + "\n\n" + members_list

    # Создаём Embed с улучшенным дизайном
    embed = disnake.Embed(
        title="🌟 Список участников организации на GitHub 🚀",
        description=f"**Организация**: {AUTHOR}\n**Владельцы**:\n{owners_list}\n\n**Mainteiners**:\n{mainteiners_list}\n\n**Остальные участники**:\n{members_list}",
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
 