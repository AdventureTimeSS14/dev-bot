import disnake
import requests
from bot_init import bot
from disnake.ext import commands
from config import AUTHOR, ACTION_GITHUB, SERVER_ADMIN_POST
from commands.misc.check_roles import has_any_role_by_id


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

    # Дополнительные поля
    embed.add_field(
        name="👤 Кто может присоединиться?",
        value="**Только члены организации** могут быть в списке участников. Если вы хотите присоединиться, пишите в https://discord.com/channels/901772674865455115/1297176881732386847.",
        inline=False
    )
    embed.add_field(
        name="📣 Внимание!",
        value="Это список всех участников организации на GitHub. Если вы хотите узнать больше информации о конкретном участнике, используйте команду &git_logininfo <login> для получения деталей о пользователе.",
        inline=False
    )

    # Отправляем Embed в канал
    await ctx.send(embed=embed)


# Функция для добавления участника в команду
def add_member_to_team(team_slug, github_login):
    """Добавляет участника в указанную команду на GitHub."""
    url = f'https://api.github.com/orgs/{AUTHOR}/teams/{team_slug}/memberships/{github_login}'

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }

    payload = {
        "role": "member"  # Можно указать "maintainer", если нужно назначить роль мейнтейнера
    }

    try:
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"❌ Ошибка при добавлении пользователя {github_login} в команду {team_slug}: {e}")
        return False


# Функция для удаления участника из команды
def remove_member_from_team(team_slug, github_login):
    """Удаляет участника из указанной команды на GitHub."""
    url = f'https://api.github.com/orgs/{AUTHOR}/teams/{team_slug}/memberships/{github_login}'

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:  # Успешное удаление возвращает 204 No Content
            return True
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Ошибка при удалении пользователя {github_login} из команды {team_slug}: {e}")
        return False


# Команда для добавления пользователя в команду adt_maintainer
@bot.command(
    name="add_maint",
    help="Добавляет пользователя в команду adt_maintainer на GitHub."
)
@has_any_role_by_id(SERVER_ADMIN_POST)
async def add_to_maintainer(ctx, github_login: str):
    """
    Добавляет пользователя в команду adt_maintainer.
    """
    team_slug = "adt_maintainer"  # Название команды

    if add_member_to_team(team_slug, github_login):
        await ctx.send(f"✅ Пользователь `{github_login}` успешно добавлен в команду `{team_slug}`.")
    else:
        await ctx.send(f"❌ Не удалось добавить пользователя `{github_login}` в команду `{team_slug}`.")


# Команда для удаления пользователя из команды adt_maintainer
@bot.command(
    name="del_maint",
    help="Удаляет пользователя из команды adt_maintainer на GitHub."
)
@has_any_role_by_id(SERVER_ADMIN_POST)
async def remove_from_maintainer(ctx, github_login: str):
    """
    Удаляет пользователя из команды adt_maintainer.
    """
    team_slug = "adt_maintainer"  # Название команды

    if remove_member_from_team(team_slug, github_login):
        await ctx.send(f"✅ Пользователь `{github_login}` успешно удалён из команды `{team_slug}`.")
    else:
        await ctx.send(f"❌ Не удалось удалить пользователя `{github_login}` из команды `{team_slug}`.")
