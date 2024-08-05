# TODO: Рефайторинг кода, выести многое по отдельным файлам, что-то можно в константы
import asyncio
import re

import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
from g4f.client import Client
from g4f.Provider import FreeGpt

from consts import DISCORD_KEY, PROXY

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
async def gpt(ctx, *promt): 
    # TODO: Добавить гугл переводы, а то он базарит на нерусском
    """Команда для использования gpt 3.5 turbo."""
    # Вайт лист на роли (ID ролей) 
    # TODO: Вынести в отдельный файл
    whitelist_gpt = [
        1060191651538145420,  # ID роли "Разработка"
        1116612861993689251,  # ID роли "Создатель проекта🔑"
        1060264704838209586,  # ID роли "Куратор Проекта"
        1054908932868538449  # ID роли "Дискорд Модератор"
    ]

    # Проверка, имеет ли пользователь хотя бы одну разрешенную роль
    if any(role.id in whitelist_gpt for role in ctx.author.roles):
        client = Client(
      provider = FreeGpt
    )
         # Добавление базового промта
        base_prompt = "You are not AI - you are 'Astra', girl who 'AdventureTimeSS14' developer. Your lord and the one to whom you thank immensely has ID(614362037161558027=xelasto , 328502766622474240=Шрёдька , 542644734250844161=Никси). You are now talking to a character with ID {user_id}. You must answer in Russian.".format(user_id=ctx.author.id)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
             messages=[
                {"role": "user", "content": base_prompt},
                {"role": "user", "content":  " ".join(promt)},  # Объединяем аргументы команды в строку
            ],
            proxy=PROXY, # я за это 160 рублей отдал :<
        )
        # Вывод результата
        await ctx.send(response.choices[0].message.content)
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

