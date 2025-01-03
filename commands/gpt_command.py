"""
Модуль gpt_command
Author: Schodinger71, Nix Silvam, Xelasto
"""

from disnake.ext import commands
from disnake.ext.commands import BucketType
from g4f.client import Client
from g4f.Provider import FreeGpt

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import GPT_PROMPT, WHITELIST_ROLE_ID


@bot.command()
@commands.cooldown(1, 60, BucketType.user)
@has_any_role_by_id(WHITELIST_ROLE_ID)
async def gpt(ctx, *prompt):
    """
    Команда принимает промт и отправляет его
    к Gpt чату, и присылает от него же ответ.

    Параметры:
    ctx: Контекст команды из Discord.
    prompt: Строка запроса, которую пользователь хочет отправить в GPT.
    """
    async with ctx.typing():
        formatted_prompt = GPT_PROMPT.format(user_id=ctx.author.id)
        client = Client(provider=FreeGpt)

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": formatted_prompt},
                    {"role": "user", "content": " ".join(prompt)},
                ],
            )
            # Отправляем ответ от GPT в канал
            await ctx.send(response.choices[0].message.content)

        except (ConnectionError, TimeoutError) as e:
            # Обработка более конкретных ошибок подключения и таймаутов
            await ctx.send(f"Ошибка при подключении к GPT: {str(e)}")
        except Exception as e:
            # Общая ошибка для всех остальных случаев
            await ctx.send(f"Произошла ошибка при обращении к GPT: {str(e)}")


@gpt.error
async def gpt_error(ctx, error):
    """
    Обработка ошибок для команды gpt.
    Проверка на тайм-ауты и ошибки проверки прав пользователя.

    Параметры:
    ctx: Контекст команды из Discord.
    error: Ошибка, возникшая при выполнении команды.
    """
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"Эту команду можно использовать снова через {int(error.retry_after)} секунд."
        )

    elif isinstance(error, commands.CheckFailure):
        await ctx.send(
            "Не могу идентифицировать вас в базе данных команды разработки Adventure Time, "
            "вы не имеете права пользоваться этой командой."
        )
