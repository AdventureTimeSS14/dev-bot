from bot_init import bot
import discord
from github import Github


@bot.command(name='milestones')
async def milestones(ctx, repo_key: str):
    """Получает информацию о всех milestones для указанного репозитория."""
    # Проверка, имеет ли пользователь хотя бы одну разрешенную роль
    if any(role.id in whitelist_role for role in ctx.author.roles):
        if repo_key not in repositories:
            await ctx.send("Пожалуйста, укажите корректный репозиторий: n или o.")
            return

        repository_name = f"{author}/{repositories[repo_key]}"
        milestones_list = await get_milestones(repository_name)

        if not milestones_list:
            await ctx.send("Milestones не найдены.")
            return

        # Делим список milestones на несколько embed, чтобы не превышать ограничение по количеству полей
        embed_list = []
        current_embed = discord.Embed(title=f"Список Milestones. \nРепозиторий: {repository_name}", color=discord.Color.blue())

        for i, milestone in enumerate(milestones_list):
            if i % 25 == 0 and i > 0:  # Создаем новый embed каждые 25 milestones
                embed_list.append(current_embed)
                current_embed = discord.Embed(title=f"Список Milestones. \nРепозиторий: {repository_name}", color=discord.Color.blue())

            current_embed.add_field(name=milestone['title'], value=f"Ссылка: {milestone['url']}\nДата завершения: {milestone['due_date']}\nЗакрытые задачи: {milestone['closed_issues']}\nОткрытые задачи: {milestone['open_issues']}\nПроцент выполнения: {milestone['completion']}", inline=False)

        embed_list.append(current_embed)  # Добавляем последний embed

        # Отправляем сообщения с embed
        for embed in embed_list:
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException as exc:
                await ctx.send(f"Ошибка: {exc}")  # Выводим ошибку в чат
    else:
        await ctx.send("Не могу идентифицировать вас в базе данных команды разработки Adventure Time, вы не имеете права пользоваться этой командой.")

async def get_milestones(repository):
    """Получает информацию о milestones репозитория и возвращает её как список словарей."""
    try:
        g = Github(GITHUB)
        repo = g.get_repo(repository)

        # Получение списка milestones
        milestones = repo.get_milestones(state='all')

        milestones_list = []
        for milestone in milestones:
            # Вычисляем процент выполнения
            if milestone.open_issues + milestone.closed_issues > 0:
                completion_percentage = (milestone.closed_issues / (milestone.open_issues + milestone.closed_issues)) * 100
            else:
                completion_percentage = 0

            milestones_list.append({
                "title": milestone.title,
                "url": milestone.url,  # Изменено на milestone.url
                "due_date": milestone.due_on,
                "completion": f"{completion_percentage:.2f}%",
                "open_issues": milestone.open_issues,
                "closed_issues": milestone.closed_issues
            })

        return milestones_list
    except Exception as e:
        print(f"Ошибка при получении milestones: {e}")
        return []