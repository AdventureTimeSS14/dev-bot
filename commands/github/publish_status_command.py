import disnake
import requests
from bot_init import bot
from config import AUTHOR, REPOSITORIES, ACTION_GITHUB
from disnake.ext import commands

# Функция для обрезки текста до 1024 символов
def truncate_text(text, max_length=1024):
    return text[:max_length - 3] + "..." if len(text) > max_length else text

# Функция для получения информации о последнем запуске workflow
def get_last_workflow_run(repository):
    url = f'https://api.github.com/repos/{AUTHOR}/{REPOSITORIES[repository]}/actions/workflows/publish-adt.yml/runs'
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"Bearer {ACTION_GITHUB}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        runs = response.json().get("workflow_runs", [])
        return runs[0] if runs else None
    except requests.RequestException:
        return None

# Функция для получения информации о шагах последнего запуска
def get_run_steps(run_id, repository):
    url = f'https://api.github.com/repos/{AUTHOR}/{REPOSITORIES[repository]}/actions/runs/{run_id}/jobs'
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"Bearer {ACTION_GITHUB}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("jobs", [])
    except requests.RequestException:
        return []

# Перевод статусов с цветами и эмодзи
def translate_status(status):
    status_translation = {
        "in_progress": ("В процессе", disnake.Color.orange(), "⏳"),
        "success": ("Успех", disnake.Color.dark_green(), "🎉"),
        "completed": ("Завершено", disnake.Color.green(), "✅"),
        "queued": ("Ожидание", disnake.Color.yellow(), "⏸️"),
        "failure": ("Неудача", disnake.Color.red(), "❌"),
    }
    return status_translation.get(status, ("Неизвестно", disnake.Color.dark_gray(), "❓"))

@bot.command(name="publish_status", help="Выводит результаты последнего запуска GitHub Actions workflow 'publish-adt.yml'.")
async def last_publish_tests(ctx, repository: str = "n"):
    if repository not in ['n', 'o']:
        await ctx.send("❌ Указан неверный репозиторий. Используйте 'n' или 'o'.")
        return

    last_run = get_last_workflow_run(repository)
    # Если last_run есть, то получаем его статус и цвет
    if last_run:
        run_status = last_run["status"]
        translated_status, embed_color, _ = translate_status(run_status)
    else:
        embed_color = disnake.Color.dark_gray()  # Цвет для неудачного или отсутствующего статуса
        translated_status = "Не удалось получить статус"

    embed = disnake.Embed(
        title="Результаты тестов Publish",
        description=f"**Репозиторий**: `{REPOSITORIES[repository]}`\n**Статус запуска**: {translated_status}",
        color=embed_color,
        timestamp=disnake.utils.utcnow()
    )

    embed.set_footer(text=f"Запрос от {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

    if last_run:
        run_id = last_run["id"]
        user, branch = last_run["actor"]["login"], last_run["head_branch"]
        embed.add_field(name="Запуск", value=f"**Пользователь**: `{user}`\n**Ветка**: `{branch}`", inline=False)

        jobs = get_run_steps(run_id, repository)
        if jobs:
            for job in jobs:
                job_name, job_status = job["name"], job["status"]
                translated_status, color, emoji = translate_status(job_status)
                description = f"**Статус**: {translated_status}"
                embed.add_field(name=f"{emoji} **Publish work**", value=truncate_text(description), inline=False)

                for step in job.get("steps", []):
                    step_name, step_status = step["name"], step["status"]
                    translated_step_status, step_color, step_emoji = translate_status(step_status)
                    step_description = f"**Статус**: {translated_step_status}"
                    embed.add_field(name=f"{step_emoji} {step_name}", value=truncate_text(step_description), inline=True)
        else:
            embed.add_field(name="❓ Нет шагов", value="Не удалось получить информацию о шагах последнего запуска.", inline=False)
    else:
        embed.add_field(name="❓ Информация о последнем запуске", value="Не удалось получить информацию о последнем запуске workflow.", inline=False)

    await ctx.send(embed=embed)
