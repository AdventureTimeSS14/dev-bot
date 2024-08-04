import asyncio
import re

import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
from g4f.client import Client

from consts import DISCORD_KEY

bot = commands.Bot(command_prefix='&', help_command=None, intents=discord.Intents.all())

repositories = {
    'n': 'space_station_ADT',
    'o': 'space_station'
}

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

# Список вариаций "обнимает"
hug_variations = [
    "*обнимает*",
    "обнимает",
    "обнимашки",
    "обними",
    "дай обнимашек",
    "прижми",
    "обниму",
    "хочу обнимашек",
    "обнял",
    "обняла"
]

author = "AdventureTimeSS14"

pattern = re.compile(r'\[(n|o)(\d+)\]')

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
    
    return f'[{repo_name} {number}]({pr_url})'  # You were returning the repository name and number, not the URL

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="📚 Помощь по командам",
        color=discord.Color.dark_green()
    )
    embed.add_field(
        name="Основные команды:",
        value="""
❓ &help - Показать это сообщение.
🏓 &pong - Ответит 'Pong!'.
🔄 &echo <сообщение> - Повторить ваше сообщение.
🎭 &user_role "<роль>" - Показать список пользователей с указанной ролью.
🤖 &gpt <промт> - ChatGPT 3.5 turbo
        """,
        inline=False
    )
    embed.add_field(
        name="Доп. возможности:",
        value="""
⏳ Всем отвечает когда будет апстрим.
🤗 Обнимает в ответ.
        """,
        inline=False
    )
    embed.add_field(
        name="Доп. информация:",
        value="""
        
✨ Если у вас есть вопросы или вам нужна помощь, 
 обращайтесь к создателю: Шрёдька :з 🖤👾
        
Разработчики:
👨‍💻 Автор: schrodinger71
👥 Maintainer: schrodinger71, nixsilvam, xelasto
📡 Хост: xelasto
        """,
        inline=False
    )
    await ctx.send(embed=embed)
    
@bot.command(name='echo')
async def echo(ctx, *, message: str):
    # Список ID пользователей, которым разрешено использовать команду
    whitelist = [328502766622474240]  # Замените на реальные ID пользователей

    # Проверяем, есть ли пользователь в белом списке
    if ctx.author.id not in whitelist:
        await ctx.send("У вас нет доступа к этой команде.")
        return

    # Удаляем сообщение пользователя
    await ctx.message.delete()

    # Отправляем эхо-сообщение
    await ctx.send(message)  
    
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

@bot.command()
async def gpt(ctx, *promt): # получение промта из аргументов
    """Команда для использования gpt 3.5 turbo."""
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # выбор модели
        messages=[{"role": "user", "content":  promt}],)
    # Вывод результата
    await ctx.send(response.choices[0].message.content)
   
@bot.event
async def on_message(message):
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return
    # Игнорируем команды бота
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return
    

    # Проверяем наличие фраз в сообщении
    if any(fuzz.ratio(message.content.lower(), phrase) >= 70 for phrase in phrases):
        await message.channel.send("Через неделю.")
        return
    # Проверка на наличие слова "апстрим" в сообщении
    if any(phrase.lower() in message.content.lower() for phrase in phrases):
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

