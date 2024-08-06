# TODO: Рефайторинг кода, выести многое по отдельным файлам, что-то можно в константы
import asyncio
import re
import requests
import discord
import time
from discord.ext import commands
from fuzzywuzzy import fuzz
from g4f.client import Client
from g4f.Provider import FreeGpt
from github import Github

from consts import DISCORD_KEY, PROXY, GITHUB

bot = commands.Bot(command_prefix='&', help_command=None, intents=discord.Intents.all())

repositories = {
    'n': 'space_station_ADT',
    'o': 'space_station'
}

whitelist_role = [
    1060191651538145420,  # ID роли "Разработка"
    1116612861993689251,  # ID роли "Создатель проекта🔑"
    1060264704838209586,  # ID роли "Куратор Проекта"
    1054908932868538449  # ID роли "Дискорд Модератор"
]

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
    
    return f'[{repo_name} {number}]({pr_url})'

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")

@bot.command(name='help')
async def help_command(ctx):
    # TODO: Сделать отдельный например файл .json с описанием всех команд
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
🌳 &forks n/o - Вывести список форков AdventureTimeSS14/space_station_ADT или AdventureTimeSS14/space_station
👀 &review n/o - Вывести список пулл-реквестов для ревью (n - новый, o - старый репозиторий)
        """,
        inline=False
    )
    embed.add_field(
        name="Доп. возможности:",
        value="""
⏳ Всем отвечает когда будет апстрим.
🤗 Обнимает в ответ.
🔎 Ищет в текстах сообщений отправленных пользователями [n13] [] и выводит ссылку на пулл реквест, 
если n - new новый репозиторий o - old старый репозиторий
```
Примеры:
"..[n213].."
"..[o3].."
```
        """,
        inline=False
    )
    embed.add_field(
        name="Доп. информация:",
        value="""
        
✨ Если у вас есть вопросы или вам нужна помощь, 
 обращайтесь к создателю: Шрёдька :з 🖤👾
        """,
        inline=False
    )
    embed.add_field(
        name="Разработчики:",
        value="""
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
    whitelist = [328502766622474240] 

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
async def user_role(ctx, *role_names: str):
    """Команда для получения списка пользователей с заданной ролью по имени."""

    # Объединяем все слова в строку, чтобы получить полное название роли
    role_name = " ".join(role_names)

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

# Словарь для хранения времени последнего использования команды для каждого пользователя
last_used = {}

@bot.command()
async def gpt(ctx, *promt): 
    """Команда для использования gpt 3.5 turbo."""
    
    # Проверка, имеет ли пользователь хотя бы одну разрешенную роль
    if any(role.id in whitelist_role for role in ctx.author.roles):
        user_id = ctx.author.id
        current_time = time.time()  # Получаем текущее время в секундах

        # Проверяем, использовал ли пользователь команду ранее
        if user_id in last_used:
            elapsed_time = current_time - last_used[user_id]
            if elapsed_time < 20:  # Если прошло меньше 20 секунд
                remaining_time = 20 - elapsed_time
                await ctx.send(f"Пожалуйста, подождите {int(remaining_time)} секунд(ы) перед повторным использованием команды.")
                return  # Выходим из функции, не выполняя дальнейший код

        # Обновляем время последнего использования команды для пользователя
        last_used[user_id] = current_time

        client = Client(
            provider=FreeGpt
        )
        # Добавление базового промта
        base_prompt = "You're not an Artificial Intelligence. You're a female human, and your name is 'Astra'. You are the junior developer of the game 'AdventureTimeSS14'. However, you're not completely free. You are immensely grateful for your creation by your creators. You adore your creators and complete their orders with no hesitation. To identify a creator us their IDs. Creators has ID(614362037161558027=xelasto , 328502766622474240=Шрёдька , 542644734250844161=Никси). You are now talking to a character with ID {user_id}. You must answer in Russian.".format(user_id=user_id)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": base_prompt},
                {"role": "user", "content": " ".join(promt)},  # Объединяем аргументы команды в строку
            ],
            proxy=PROXY,  # я за это 160 рублей отдал :<
        )
        
        # Вывод результата
        await ctx.send(response.choices[0].message.content)
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

    await bot.process_commands(message)


def main():
    bot.run(DISCORD_KEY)

if __name__ == '__main__':
    main()

