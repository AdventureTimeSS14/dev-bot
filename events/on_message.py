import re

from fuzzywuzzy import fuzz

from bot_init import bot


@bot.event
async def on_message(message):
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return
    # Игнорируем команды бота
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    if any(fuzz.token_sort_ratio(message.content.lower(), phrase) >= 70 for phrase in phrases):
        await message.channel.send("Через неделю.")
        return
    
    if f"<@{bot.user.id}>" in message.content:
        # Извлекаем текст без упоминания бота
        text_without_mention = message.content.replace(f"<@{bot.user.id}>", "").strip()
        # Проверяем, содержит ли текст любую вариацию "обнимает"
        for variation in hug_variations:
            if fuzz.token_sort_ratio(text_without_mention.lower(), variation) > 80:
                await message.channel.send("*Обнимает в ответ.*")
                break  # Прерываем цикл после отправки сообщения
    
    # Ищем паттерн в сообщении
    match = re.compile(r'\[(n|o)(\d+)\]').search(message.content)
    if match:
        repo_code, number = match.groups()
        link = check_github_issue_or_pr(repo_code, number)
        if link:
            await message.channel.send(f'{link}')

def check_github_issue_or_pr(repo_code, number):
    """
    Возвращает ссылку на GitHub issue или PR в зависимости от введенного кода репозитория (n или o).

    Args:
        repo_code: Код репозитория (n или o).
        number: Номер issue или PR.

    Returns:
        Ссылка на GitHub issue или PR, если она найдена, иначе None.
    """
    repo_name = repositories.get(repo_code)
    if not repo_name:
        return None

    base_url = f'https://github.com/{author}/{repo_name}'
    issue_url = f'{base_url}/issues/{number}'
    pr_url = f'{base_url}/pull/{number}'
    
    return f'[{repo_name} {number}]({pr_url})'