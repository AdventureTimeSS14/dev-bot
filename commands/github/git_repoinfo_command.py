import requests
import disnake
from disnake.ext import commands
from bot_init import bot
from config import AUTHOR, ACTION_GITHUB


# Функция для получения информации о репозитории
def get_github_repo_info(repo):
    """Получает информацию о репозитории GitHub."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        return repo_data
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении информации о репозитории: {e}")
        return None

# Функция для получения количества открытых Issues и Pull Requests
def get_repo_issues_pr_count(repo):
    """Получает количество открытых Issues и Pull Requests."""
    url_issues = f'https://api.github.com/repos/{AUTHOR}/{repo}/issues'
    url_prs = f'https://api.github.com/repos/{AUTHOR}/{repo}/pulls'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response_issues = requests.get(url_issues, headers=headers)
        response_prs = requests.get(url_prs, headers=headers)
        response_issues.raise_for_status()
        response_prs.raise_for_status()
        
        issues = response_issues.json()
        prs = response_prs.json()
        
        open_issues = len([issue for issue in issues if 'pull_request' not in issue])
        open_prs = len([pr for pr in prs])
        
        return open_issues, open_prs
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении количества Issues и Pull Requests: {e}")
        return 0, 0

# Функция для получения статистики контрибьюторов
def get_github_repo_stats(repo):
    """Получает количество контрибьюторов репозитория."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}/contributors'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        contributors = response.json()
        return len(contributors)
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении статистики контрибьюторов: {e}")
        return 0


# Функция для получения информации о последних коммитах
def get_last_commits(repo):
    """Получает информацию о последних коммитах репозитория."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}/commits'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        commits = response.json()
        if commits:
            last_commit = commits[0]
            commit_msg = last_commit.get('commit', {}).get('message', 'Нет сообщения')
            commit_date = last_commit.get('commit', {}).get('committer', {}).get('date', 'Не указана дата')
            return commit_msg, commit_date
        return 'Нет коммитов', 'Не указана дата'
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении последних коммитов: {e}")
        return 'Ошибка', 'Ошибка'


def get_repo_licenses(repo):
    """Получает все лицензии репозитория."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}/license'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        license_data = response.json()
        
        # Проверяем, есть ли несколько лицензий
        licenses = license_data.get('licenses', [])
        
        # Если лицензии есть, возвращаем их
        if licenses:
            return [license.get('name', 'Не указана лицензия') for license in licenses]
        else:
            return ['Не указана лицензия']
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении лицензий: {e}")
        return ['Не указана лицензия']


# Функция для получения количества форков
def get_forks_count(repo):
    """Получает количество форков репозитория."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        return repo_data.get('forks_count', 0)
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении количества форков: {e}")
        return 0

# Функция для получения количества обсуждений
def get_discussions_count(repo):
    """Получает количество обсуждений в репозитории."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}/discussions'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        discussions = response.json()
        return len(discussions)
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении количества обсуждений: {e}")
        return 0

# Функция для получения количества релизов
def get_releases_count(repo):
    """Получает количество релизов репозитория."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}/releases'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        releases = response.json()
        return len(releases)
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении количества релизов: {e}")
        return 0

# Функция для получения размера репозитория
def get_repo_size(repo):
    """Получает размер репозитория в байтах и конвертирует в МБ."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        size_in_bytes = repo_data.get('size', 0)
        size_in_mb = size_in_bytes / (1024 * 1024)  # Переводим в мегабайты
        return round(size_in_mb, 2)
    except requests.RequestException as e:
        print(f"❌ Ошибка при получении размера репозитория: {e}")
        return 0

@bot.command(
    name="git_repoinfo",
    help="Выводит информацию о репозитории AdventureTimeSS14/space_station_ADT."
)
async def git_repoinfo(ctx):
    """
    Команда для вывода информации о репозитории AdventureTimeSS14/space_station_ADT.
    """
    repo = 'space_station_ADT'  # Указываем репозиторий для получения информации
    repo_info = get_github_repo_info(repo)

    if not repo_info:
        await ctx.send("❌ Не удалось получить информацию о репозитории.")
        return

    # Получаем количество открытых Issues и Pull Requests
    open_issues, open_prs = get_repo_issues_pr_count(repo)

    # Получаем дополнительные статистики
    contributors = get_github_repo_stats(repo)

    # Получаем информацию о последних коммитах
    last_commit_msg, last_commit_date = get_last_commits(repo)

    # Получаем информацию о лицензии
    repo_license = get_repo_licenses(repo)

    # Получаем количество форков
    forks_count = get_forks_count(repo)

    # Получаем количество обсуждений
    discussions_count = get_discussions_count(repo)

    # Получаем количество релизов
    releases_count = get_releases_count(repo)

    # Получаем размер репозитория
    repo_size = get_repo_size(repo)

    # Создаём Embed с красивым дизайном
    embed = disnake.Embed(
        title=f"Информация о репозитории {repo} 📦",
        description=f"**Организация**: `{AUTHOR}`\n**Репозиторий**: `{repo}`",
        color=disnake.Color.dark_gold(),
        timestamp=disnake.utils.utcnow()
    )

    # Добавляем основную информацию о репозитории
    embed.add_field(
        name="📝 Основная информация",
        value=(
            f"**Описание**: {repo_info.get('description', 'Нет описания')}\n"
            f"**Создан**: {repo_info.get('created_at', 'Не указано')}\n"
            f"**Обновлен**: {repo_info.get('updated_at', 'Не указано')}\n"
            f"**Звезды**: {repo_info.get('stargazers_count', 'Не указано')}\n"
            f"**Форки**: {forks_count}\n"
            f"**Язык**: {repo_info.get('language', 'Не указано')}"
        ),
        inline=False
    )

    # Добавляем количество открытых Issues и Pull Requests
    embed.add_field(
        name="🔧 Открытые Issues и PR",
        value=(
            f"**Открытые Issues**: {open_issues}\n"
            f"**Открытые Pull Requests**: {open_prs}"
        ),
        inline=False
    )

    # Добавляем статистику контрибьюторов
    embed.add_field(
        name="💻 Контрибьюторы",
        value=f"**Количество контрибьюторов**: {contributors}",
        inline=False
    )

    # Добавляем информацию о лицензии
    embed.add_field(
        name="🔒 Лицензия",
        value=repo_license,
        inline=False
    )

    # Добавляем количество обсуждений и релизов
    embed.add_field(
        name="💬 Обсуждения и релизы",
        value=(
            f"**Количество обсуждений**: {discussions_count}\n"
            f"**Количество релизов**: {releases_count}"
        ),
        inline=False
    )
    
    embed.set_footer(text=f"Запрос от {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

    # Отправляем сообщение с информацией
    await ctx.send(embed=embed)
