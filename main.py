import asyncio
import re

import discord
from discord.ext import commands
from fuzzywuzzy import fuzz

from consts import DISCORD_KEY

bot = commands.Bot(command_prefix='&', help_command=None, intents=discord.Intents.all())

repositories = {
    'n': 'space_station_ADT',
    'o': 'space_station'
}

author = "AdventureTimeSS14"
github_link = "https://github.com/"

pattern = re.compile(r'\[(s|c|t)(\d+)\]')

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

    base_url = f'{github_link}{author}/{repo_name}'
    issue_url = f'{base_url}/issues/{number}'
    pr_url = f'{base_url}/pull/{number}'
    
    return f'{repo_name} {number}'  # You were returning the repository name and number, not the URL

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")

@bot.command()
async def pong(ctx):  # должна выводить пинг бота задержку инента
    latency = round(bot.latency * 1000)  # задержка в миллисекундах
    await ctx.send(f'Pong! Задержка: {latency}ms')

@bot.command()
async def user_role(ctx, role_name: str):
    """Команда для получения списка пользователей с заданной ролью по имени."""

    # Поиск роли по названию 
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    # Проверка, найдена ли роль
    if role is None:
        await ctx.send(f"Роль '{role_name}' не найдена.")
        return

    # Получение списка участников с этой ролью
    members_with_role = [member.name for member in role.members]

    # Вывод результата
    if members_with_role:
        await ctx.send(f'Пользователи с ролью {role.name}: {", ".join(members_with_role)}')
    else:
        await ctx.send(f'Нет пользователей с ролью {role.name}.')
        
@bot.event
async def on_message(message):
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return
    # Игнорируем команды бота
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return
    
    # Список фраз, которые нужно проверять
    phrases = [
        "когда апстрим?",
        "апстрим когда?",
        "когда будет апстрим?",
        "Апстрим?",
        "как апстрим?",
        "чо по апстриму",
        "апстримчикк?",
        "Апстрим скоро?",
        "Скоро там апстрим?",
        "Апстрим когда?",
        "Апстрим",
        "upstream",
    ]
    # Проверяем наличие фраз в сообщении
    if any(fuzz.ratio(message.content.lower(), phrase) >= 70 for phrase in phrases):
        await message.channel.send("Через неделю.")
        return
    # Проверка на наличие слова "апстрим" в сообщении
    if any(phrase.lower() in message.content.lower() for phrase in phrases):
        await message.channel.send("Через неделю.")
        return
    
    # Ищем паттерн в сообщении
    match = pattern.search(message.content)
    if match:
        repo_code, number = match.groups()
        link = check_github_issue_or_pr(repo_code, number)
        if link:
            await message.channel.send(f'{link}')

    # This line should be outside the 'if match' block, so the bot still processes commands
    await bot.process_commands(message)
    
    
    # # Проверяем, является ли сообщение текстом в квадратных скобках
    # if message.content.startswith('[') and message.content.endswith(']'):
    #     pr_number = message.content[1:-1]  # Убираем квадратные скобки

    #     # Проверка на соответствие формату
    #     pattern = re.compile(r'\[(s|c|t)(\d+)\]')
    #     if re.match(pattern, pr_number):
    #         if pr_number.startswith('n'):  # Если номер начинается с 'n'
    #             link = f"{link_new}{pr_number[1:]}"  # Убираем 'n' и формируем ссылку
    #             await message.channel.send(f"[space_station_ADT PR: {pr_number}]({link})")
    #         elif pr_number.startswith('o'):  # Если номер начинается с 'o'
    #             link = f"{link_old}{pr_number[1:]}"  # Убираем 'o' и формируем ссылку
    #             await message.channel.send(f"[space_station PR: {pr_number}]({link})")
    #     else:
    #         await message.channel.send("Некорректный формат номера пулл-реквеста. Используйте например [n123] или [o342].")

def main():
    bot.run(DISCORD_KEY)

if __name__ == '__main__':
    main()

