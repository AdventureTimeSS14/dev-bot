import disnake
import aiohttp
from bot_init import bot
from config import AUTHOR, ACTION_GITHUB, REPOSITORIES
from disnake.ext import commands

# Функция для получения статистики пользователя по GitHub
async def get_github_user_info(username):
    """Получает информацию о пользователе GitHub асинхронно."""
    url = f'https://api.github.com/users/{username}'
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                user_info = await response.json()
                return user_info
    except aiohttp.ClientError as e:
        print(f"❌ Ошибка при получении информации о пользователе: {e}")
        return None

# Функция для получения всех пулл-реквестов пользователя в репозитории (с пагинацией)
async def get_github_pull_requests(username, repo):
    """Получает пулл-реквесты, связанные с пользователем в репозитории асинхронно (с пагинацией)."""
    url = f'https://api.github.com/repos/{AUTHOR}/{repo}/pulls?state=all&per_page=100&page=1'
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACTION_GITHUB}"
    }
    
    all_pull_requests = []
    while url:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    pull_requests = await response.json()
                    all_pull_requests.extend(pull_requests)

                    # Проверяем наличие следующей страницы через заголовки ответа
                    if 'link' in response.headers and 'rel="next"' in response.headers['link']:
                        # Получаем ссылку на следующую страницу
                        url = response.headers['link'].split(';')[0][1:-1]  # Извлекаем URL
                    else:
                        break  # Если нет следующей страницы, выходим из цикла
        except aiohttp.ClientError as e:
            print(f"❌ Ошибка при получении пулл-реквестов: {e}")
            break

    # Фильтруем пулл-реквесты по авторству
    user_pull_requests = [pr for pr in all_pull_requests if pr['user']['login'] == username]
    return user_pull_requests

# Функция для подсчета количества ревью в пулл-реквестах
async def get_github_reviews(pr_url):
    """Получает количество ревью для пулл-реквеста асинхронно."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{pr_url}/reviews', headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {ACTION_GITHUB}"
            }) as response:
                response.raise_for_status()
                reviews = await response.json()
                print(f"Reviews for PR {pr_url}: {len(reviews)}")
                return len(reviews)  # Подсчитываем количество ревью
    except aiohttp.ClientError as e:
        print(f"❌ Ошибка при получении ревью для пулл-реквеста: {e}")
        return 0

# Функция для подсчета количества дискуссий в пулл-реквестах
async def get_github_discussions(pr_url):
    """Получает количество дискуссий для пулл-реквеста асинхронно."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{pr_url}/comments', headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {ACTION_GITHUB}"
            }) as response:
                response.raise_for_status()
                discussions = await response.json()
                print(f"Discussions for PR {pr_url}: {len(discussions)}")
                return len(discussions)  # Подсчитываем количество комментариев
    except aiohttp.ClientError as e:
        print(f"❌ Ошибка при получении комментариев для пулл-реквеста: {e}")
        return 0

@bot.command(
    name="git_logininfo",
    help="Выводит краткую статистику о пользователе и его вкладе в репозиторий."
)
async def git_logininfo(ctx, username: str):
    """
    Команда для вывода статистики пользователя по логину и его вкладе в репозиторий.
    """
    print(f"Получение информации о пользователе {username}...")
    user_info = await get_github_user_info(username)

    if not user_info:
        await ctx.send("❌ Не удалось получить информацию о пользователе. Проверьте правильность логина.")
        return

    # Получаем пулл-реквесты, связанные с пользователем
    repo = 'space_station_ADT'  # Указываем репозиторий для получения вклада
    print(f"Получение пулл-реквестов для пользователя {username} из репозитория {repo}...")
    user_pull_requests = await get_github_pull_requests(username, repo)

    # Инициализируем счетчики для различных типов пулл-реквестов
    merged_prs = 0
    closed_prs = 0
    open_prs = 0
    draft_prs = 0
    total_reviews = 0
    total_discussions = 0

    for pr in user_pull_requests:
        pr_state = pr['state']
        pr_url = pr['url']

        # Подсчитываем количество пулл-реквестов по состояниям
        if pr_state == 'closed' and pr['merged_at']:  # Если пулл-реквест был замержен
            merged_prs += 1
        elif pr_state == 'closed':  # Если пулл-реквест был закрыт
            closed_prs += 1
        elif pr_state == 'open':  # Если пулл-реквест открыт
            open_prs += 1
        elif pr_state == 'draft':  # Если пулл-реквест в драфте
            draft_prs += 1

        # Получаем количество ревью и дискуссий для каждого пулл-реквеста
        total_reviews += await get_github_reviews(pr_url)
        total_discussions += await get_github_discussions(pr_url)

    # Создаём Embed с красивым дизайном
    embed = disnake.Embed(
        title=f"Информация о пользователе GitHub: {username} 👤",
        description=f"**Имя пользователя**: `{username}`\n**Организация**: `{AUTHOR}`",
        color=disnake.Color.green(),
        timestamp=disnake.utils.utcnow()
    )

    # Добавляем основную информацию о пользователе
    embed.add_field(
        name="📝 Основная информация",
        value=f"**Имя**: {user_info.get('name', 'Не указано')}\n"
              f"**Подписки**: {user_info.get('following', 'Не указано')}\n"
              f"**Подписчики**: {user_info.get('followers', 'Не указано')}\n"
              f"**Репозитории**: {user_info.get('public_repos', 'Не указано')}",
        inline=False
    )

    # Добавляем информацию о вкладе в репозиторий
    embed.add_field(
        name="🔧 Вклад в репозиторий",
        value=f"**Замерженные пулл-реквесты**: {merged_prs}\n"
              f"**Закрытые пулл-реквесты**: {closed_prs}\n"
              f"**Открытые пулл-реквесты**: {open_prs}\n"
              f"**Пулл-реквесты в драфте**: {draft_prs}\n"
              f"**Общее количество ревью**: {total_reviews}\n"
              f"**Общее количество дискуссий**: {total_discussions}",
        inline=False
    )

    # Добавляем аватар пользователя
    embed.set_thumbnail(url=user_info.get('avatar_url', 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'))
    embed.set_footer(text=f"Запрос от {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    
    # Отправляем Embed в канал
    await ctx.send(embed=embed)

