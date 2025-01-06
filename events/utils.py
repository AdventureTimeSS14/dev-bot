import disnake
import requests
from datetime import datetime
from config import (
    AUTHOR,
    GLOBAL_SESSION,
    REPOSITORIES,
)

async def get_github_link(repo_code, number):
    """
    Проверяет существование GitHub issue или PR и возвращает ссылку.
    """
    repo_name = REPOSITORIES.get(repo_code)
    if not repo_name:
        print(f"⚠️ Репозиторий с кодом {repo_code} не найден.")
        return None

    base_api_url = f"https://api.github.com/repos/{AUTHOR}/{repo_name}"
    pr_url = f"{base_api_url}/pulls/{number}"

    try:
        # Проверка PR
        pr_response = GLOBAL_SESSION.get(pr_url)
        if pr_response.status_code == 200:
            pr_data = pr_response.json()

            # Определение цвета в зависимости от состояния PR
            state = pr_data['state']
            merged = pr_data.get('merged', False)
            draft = pr_data.get('draft', False)

            if state == 'closed' and merged:
                state_description = "Замерджен 💜"
                embed_color = disnake.Color.purple()
            elif state == 'closed' and not merged:
                state_description = "Закрыт ❌"
                embed_color = disnake.Color.red()
            elif state == 'open' and draft:
                state_description = "В драфте ⚙️"
                embed_color = disnake.Color.darker_gray()
            elif state == 'open':
                state_description = "Открыт ✅"
                embed_color = disnake.Color.green()
            else:
                state_description = "Неизвестный статус ❓"
                embed_color = disnake.Color.default()

            # Создаем embed
            embed = disnake.Embed(
                title=f"PR #{number} - {pr_data['title']}",
                color=embed_color
            )

            embed.add_field(name="Статус PR", value=state_description, inline=True)

            # Создатель PR
            embed.add_field(name="Создатель PR 👨‍💻", value=pr_data['user']['login'], inline=True)

            # Ревьюеры
            requested_reviewers = pr_data.get('requested_reviewers', [])
            # Извлекаем только login каждого ревьюера
            requested_reviewers_logins = [reviewer['login'] for reviewer in requested_reviewers]

            # Получаем информацию о том, кто поставил отзыв
            reviews_url = f"{pr_url}/reviews"
            reviews_response = GLOBAL_SESSION.get(reviews_url)
            if reviews_response.status_code == 200:
                reviews_data = reviews_response.json()
                # Извлекаем только login ревьюеров, которые оставили отзывы
                reviewed_reviewers_logins = [review['user']['login'] for review in reviews_data]

                # Объединяем список назначенных и тех, кто уже поставил отзыв (не повторяем)
                all_reviewers = set(requested_reviewers_logins + reviewed_reviewers_logins)  # Теперь это список логинов
                all_reviewers_str = ', '.join(all_reviewers) if all_reviewers else "Нет ревьюеров"

                # Добавляем информацию о всех ревьюерах
                embed.add_field(name="Ревьюеры 🔍", value=all_reviewers_str, inline=True)
            else:
                embed.add_field(name="Ревьюеры 🔍", value=", ".join(requested_reviewers_logins), inline=True)

            # Информация о том, кто одобрил (approved) PR
            reviews_url = f"{pr_url}/reviews"
            reviews_response = GLOBAL_SESSION.get(reviews_url)
            if reviews_response.status_code == 200:
                reviews_data = reviews_response.json()
                approved_reviewers = [review['user']['login'] for review in reviews_data if review['state'] == 'APPROVED']
                if approved_reviewers:
                    approved_reviewers_str = ', '.join(approved_reviewers)
                    embed.add_field(name="Одобрение 🌟", value=approved_reviewers_str, inline=True)
                else:
                    embed.add_field(name="Одобрение 🌟", value="Нет одобрений", inline=True)

            # Метки (Labels)
            labels = pr_data.get('labels', [])
            labels_str = ', '.join([f"[{label['name']}]" for label in labels]) if labels else "Нет меток 🏷️"
            embed.add_field(name="Метки 🏷️", value=labels_str, inline=True)

            # Количество комментариев
            comments_count = pr_data['comments']
            embed.add_field(name="Комментарии 💬", value=comments_count, inline=True)

            # Получаем информацию о количестве добавленных и удалённых строк
            diffstat_url = f"{pr_url}/files"
            diffstat_response = GLOBAL_SESSION.get(diffstat_url)
            if diffstat_response.status_code == 200:
                diffstat_data = diffstat_response.json()
                added_lines = sum(file['additions'] for file in diffstat_data)
                deleted_lines = sum(file['deletions'] for file in diffstat_data)
                # Добавляем изменения строк в нужном формате
                embed.add_field(name="Изменение строк 🔄", value=f"Добавлено: +{added_lines}\nУдалено: −{deleted_lines}", inline=True)


            # Форматируем даты в более читаемый вид
            created_at = datetime.strptime(pr_data['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            updated_at = datetime.strptime(pr_data['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            closed_at = pr_data.get('closed_at')  # Дата закрытия (если PR закрыт)
            closed_at_str = ""
            if closed_at:
                closed_at = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
                closed_at_str = closed_at.strftime("• Закрыт {0}".format(closed_at.strftime("%d %b %Y, %H:%M")))

            created_at_str = created_at.strftime("%d %b %Y, %H:%M")  # Например, 30 Jun 2024, 09:59
            updated_at_str = updated_at.strftime("%d %b %Y, %H:%M")  # Например, 30 Jun 2024, 12:16

            # Дополнительная информация о PR с улучшенным форматированием
            embed.set_footer(text=f"PR открыт {created_at_str} • Обновлен {updated_at_str} {closed_at_str}")

            # Завершающие теги
            if draft:
                embed.set_footer(text=f"Этот PR в работе. #WIP ⚙️ • {updated_at_str}")

            # Ссылка на PR
            embed.add_field(name="Ссылка на PR 🔗", value=f"[Перейти в PR]({pr_data['html_url']})", inline=False)

            return embed

        # Если PR не найден, пытаемся искать Issue
        issue_url = f"{base_api_url}/issues/{number}"
        issue_response = GLOBAL_SESSION.get(issue_url)
        if issue_response.status_code == 200:
            issue_data = issue_response.json()
            return f"[{repo_name} Issue {number}]({issue_data['html_url']})"

    except requests.RequestException as e:
        print(f"❌ Ошибка при запросе к GitHub API: {e}")

    return None