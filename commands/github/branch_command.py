import disnake
import requests
from bot_init import bot
from config import AUTHOR, REPOSITORIES

# URL для получения списка веток репозитория
def get_branches_url(repository):
    """Генерация URL для запроса к GitHub API для получения списка веток."""
    return f'https://api.github.com/repos/{AUTHOR}/{REPOSITORIES[repository]}/branches'

def fetch_branches_data(url):
    """Получение данных о ветках с GitHub."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Ошибка при выполнении запроса к GitHub API: {e}")
        return None

@bot.command(
    name="branch",
    help="Получить список веток репозитория. По умолчанию выводятся ветки репозитория 'n', можно указать 'n' или 'o'.",
)
async def get_branches(ctx, repository: str = "n"):
    """
    Команда для получения списка веток репозитория 'n' или 'o'.
    Если не указан репозиторий, по умолчанию будет выбран 'n'.
    """
    if repository not in ['n', 'o']:
        await ctx.send("❌ Указан неверный репозиторий. Используйте 'n' или 'o'.")
        return

    url = get_branches_url(repository)
    branches = fetch_branches_data(url)

    if not branches:
        await ctx.send("❌ Не удалось получить список веток.")
        return

    # Формируем строку с ветками
    branch_names = [branch["name"] for branch in branches]
    branches_list = "\n".join(branch_names)

    # Создаём Embed с улучшенным дизайном
    embed = disnake.Embed(
        title=f"Список веток репозитория {REPOSITORIES[repository]}",
        description=f"Список веток репозитория `{REPOSITORIES[repository]}`.",
        color=disnake.Color.green(),
        timestamp=disnake.utils.utcnow()
    )

    # Эмодзи и стили
    embed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    embed.set_footer(text=f"Запрос от {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

    # Заголовок и список веток
    embed.add_field(
        name="🚀 Ветки репозитория:",
        value=branches_list if branches_list else "❌ Нет веток",
        inline=False
    )

    # Отправляем Embed в канал
    await ctx.send(embed=embed)
