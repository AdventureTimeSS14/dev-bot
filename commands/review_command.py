import discord
from github import Github

from bot_init import bot


@bot.command(name='review')
async def review(ctx, repo_key: str):
    """Получает пулл-реквесты для указанного репозитория, требующие ревью."""
    # Проверка, имеет ли пользователь хотя бы одну разрешенную роль
    if any(role.id in whitelist_role for role in ctx.author.roles):
        if repo_key not in repositories:
            await ctx.send("Пожалуйста, укажите корректный репозиторий: n или o.")
            return

        repository_name = f"{author}/{repositories[repo_key]}"
        pull_requests_list = await get_pull_requests(repository_name)

        if not pull_requests_list:
            await ctx.send("Пулл-реквесты не найдены или не требуют ревью.")
            return

        # Делим список пулл-реквестов на несколько embed, чтобы не превышать ограничение по количеству полей
        embed_list = []
        current_embed = discord.Embed(title=f"Список пулл-реквестов для ревью. \nРепозиторий: {repository_name}", color=discord.Color.dark_red())
        
        for i, pr in enumerate(pull_requests_list):
            if i % 25 == 0 and i > 0:  # Создаем новый embed каждые 25 пулл-реквестов
                embed_list.append(current_embed)
                current_embed = discord.Embed(title=f"Список пулл-реквестов для ревью. \nРепозиторий: {repository_name}", color=discord.Color.dark_red())

            requested_by = ', '.join(pr['requested_by']) if pr['requested_by'] else 'Нет запрашиваемых рецензентов'  # Преобразуем список в строку
            current_embed.add_field(name=pr['title'], value=f"Автор: {pr['author']}\nЧьё ревью запрошено: {requested_by}\nСсылка: {pr['url']}", inline=False)

        embed_list.append(current_embed)  # Добавляем последний embed

        # Отправляем сообщения с embed
        for embed in embed_list:
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException as exc:
                await ctx.send(f"Ошибка: {exc}")  # Выводим ошибку в чат
    else:
        await ctx.send("Не могу идентифицировать вас в базе данных команды разработки Adventure Time, вы не имеете права пользоваться этой командой.")

async def get_pull_requests(repository):
    """Получает информацию о пулл-реквестах, требующих ревью, и возвращает её как список словарей."""
    try:
        g = Github(GITHUB)
        repo = g.get_repo(repository)

        # Получение списка пулл-реквестов, которые требуют ревью
        pulls = repo.get_pulls(state='open', sort='created', base='master')
        
        pull_requests_list = []
        for pr in pulls:
            # Проверяем наличие метки "Status: Needs Review"
            if any(label.name == "Status: Needs Review" for label in pr.labels):
                pull_requests_list.append({
                    "title": pr.title,
                    "url": pr.html_url,
                    "author": pr.user.login,
                    "requested_by": [reviewer.login for reviewer in pr.requested_reviewers]  # Получаем имена тех, кто запросил ревью
                })

        return pull_requests_list

    except Exception as e:
        print(f"Ошибка при получении пулл-реквестов: {e}")
        return []
