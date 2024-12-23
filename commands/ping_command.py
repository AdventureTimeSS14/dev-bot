from bot_init import bot


@bot.command(name="ping", help="Проверяет задержку бота.")
async def ping(ctx):
    """
    Команда для проверки задержки бота.
    """
    latency = round(bot.latency * 1000)  # Вычисляем задержку в миллисекундах
    emoji = "🏓" if latency < 100 else "🐢"  # Выбираем эмодзи в зависимости от задержки
    await ctx.send(f"{emoji} Pong! Задержка: **{latency}ms**")
