from bot_init import bot


@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")