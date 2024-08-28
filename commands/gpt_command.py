from discord.ext import commands
from discord.ext.commands import BucketType
from g4f.client import Client
from g4f.Provider import FreeGpt

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from config import GPT_PROMPT, WHITELIST_ROLE_ID


@bot.command()
@commands.cooldown(1, 60, BucketType.user)
@has_any_role_by_id(WHITELIST_ROLE_ID)
async def gpt(ctx, *prompt): 
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
                # proxy=PROXY,
            )
            
            await ctx.send(response.choices[0].message.content)

        except Exception as e:
            await ctx.send(f"Произошла ошибка при обращении к GPT: {str(e)}")
        
@gpt.error
async def gpt_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Эту команду можно использовать снова через {int(error.retry_after)} секунд.")  
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Не могу идентифицировать вас в базе данных команды разработки Adventure Time, вы не имеете права пользоваться этой командой.")
    commands.MissingRequiredArgument