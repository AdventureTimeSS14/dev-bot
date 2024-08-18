import time

from g4f.client import Client
from g4f.Provider import FreeGpt

from bot_init import bot
from config import GPT_PROMPT, PROXY, WHITELIST_ROLE_ID

last_used = {}

@bot.command()
async def gpt(ctx, *prompt): 
    if not any(role.id in WHITELIST_ROLE_ID for role in ctx.author.roles):
        await ctx.send("Не могу идентифицировать вас в базе данных команды разработки Adventure Time, вы не имеете права пользоваться этой командой.")
        return
    
    user_id = ctx.author.id
    current_time = time.time()

    if user_id in last_used:
        elapsed_time = current_time - last_used[user_id]
        if elapsed_time < 20:
            remaining_time = 20 - elapsed_time
            await ctx.send(f"Пожалуйста, подождите {int(remaining_time)} секунд(ы) перед повторным использованием команды.")
            return

    last_used[user_id] = current_time
    
    formatted_prompt = GPT_PROMPT.format(user_id=user_id)
    client = Client(provider=FreeGpt)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": formatted_prompt},
                {"role": "user", "content": " ".join(prompt)},
            ],
            proxy=PROXY,  # я за это 160 рублей отдал :<
        )
        
        await ctx.send(response.choices[0].message.content)

    except Exception as e:
        await ctx.send(f"Произошла ошибка при обращении к GPT: {str(e)}")