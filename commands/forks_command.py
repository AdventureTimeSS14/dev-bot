from bot_init import bot
import discord
from github import Github

@bot.command(name='forks')
async def forks(ctx, repo_key: str):
    """Получает форки для указанного репозитория."""
    # Проверка, имеет ли пользователь хотя бы одну разрешенную роль
    if any(role.id in whitelist_role for role in ctx.author.roles):
        if repo_key not in repositories:
            await ctx.send("Пожалуйста, укажите корректный репозиторий: n или o.")
            return

        repository_name = f"{author}/{repositories[repo_key]}"
        forks_list = await get_forks(repository_name)

        if not forks_list:
            await ctx.send("Форки не найдены.")
            return

        # Делим список форков на несколько embed, чтобы не превышать ограничение по количеству полей
        embed_list = []
        current_embed = discord.Embed(title=f"Список форков для репозитория {repository_name}", color=discord.Color.dark_green())
        
        for i, fork in enumerate(forks_list):
            if i % 25 == 0 and i > 0:  # Создаем новый embed каждые 25 форков
                embed_list.append(current_embed)
                current_embed = discord.Embed(title=f"Список форков для репозитория {repository_name}", color=discord.Color.dark_green())

            current_embed.add_field(name=fork['name'], value=f"Владелец: {fork['owner']}\nСсылка: {fork['url']}", inline=False)

        embed_list.append(current_embed)  # Добавляем последний embed

        # Отправляем сообщения с embed
        for embed in embed_list:
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException as exc:
                await ctx.send(f"Ошибка: {exc}")  # Выводим ошибку в чат
    else:
        await ctx.send("Не могу идентифицировать вас в базе данных команды разработки Adventure Time, вы не имеете права пользоваться этой командой.")
        
        
async def get_forks(repository):
    """Получает информацию о форках репозитория и возвращает её как список словарей."""
    try:
        g = Github(GITHUB)
        repo = g.get_repo(repository)

        # Базовый URL для запросов к API
        base_url = f'https://api.github.com/repos/{repository}'
        session = requests.Session()

        # Получение списка форков с пользователями
        forks_list = []
        forks_url = f'{base_url}/forks'
        forks_response = session.get(forks_url)
        forks_response.raise_for_status()

        # Обработка ограничения по количеству форков
        forks_count = 0
        for fork in forks_response.json():
            forks_list.append({
                "name": fork['full_name'],
                "owner": fork['owner']['login'],
                "url": fork['html_url']
            })
            forks_count += 1
            if forks_count >= 25:  # Ограничение по количеству полей в embed
                break

        return forks_list

    except Exception as e:
        print(f"Ошибка при получении информации о форках: {e}")
        return []
