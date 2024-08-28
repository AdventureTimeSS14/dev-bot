from bot_init import bot


@bot.command(name='echo')
async def echo(ctx, *, message: str):
    if ctx.author.id != 328502766622474240:
        await ctx.send("У вас нет доступа к этой команде.")
        return

    await ctx.message.delete()

    await ctx.send(message)