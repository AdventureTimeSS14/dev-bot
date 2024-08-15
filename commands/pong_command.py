from bot_init import bot

@bot.command()
async def pong(ctx):  # должна выводить пинг бота задержку инента
    latency = round(bot.latency * 1000)  # задержка в миллисекундах
    await ctx.send(f'Pong! Задержка: {latency}ms')