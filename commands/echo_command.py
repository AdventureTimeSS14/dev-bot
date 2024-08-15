from bot_init import bot

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