import discord

from bot_init import bot


async def shutdown_def():
    channel_id = 1320771026019422329  # ID канала, где нужно редактировать сообщение
    message_id = 1320771150938243195  # ID сообщения, которое нужно редактировать
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    # Редактируем отправленное сообщение
    await message.edit(content=f"{bot.user} отключена!")
    
    
    ss14_address = "ss14://193.164.18.155"
    channel_id = 1320771026019422329  # ID канала
    message_id = 1320771122433622084  # ID сообщения
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    embed = discord.Embed(color=discord.Color.red())
    embed.title = "Ошибка получения данных"
    embed.add_field(name="Игроков", value="Error!", inline=False)
    embed.add_field(name="Статус", value="Error!", inline=False)
    embed.add_field(name="Время раунда", value="Error!", inline=False)
    embed.add_field(name="Раунд", value="Error!", inline=False)
    embed.add_field(name="Карта", value="Error!", inline=False)
    embed.add_field(name="Режим игры", value="Error!", inline=False)
    embed.add_field(name="Бункер", value="Error!", inline=False)
    embed.set_footer(text=f"Адрес: {ss14_address}")
    await message.edit(embed=embed)
    
    name = "Отключена!"
    status_state = f"Игроков: ERROR! | Режим: ERROR! | Раунд: ERROR! | Статус: ERROR!"  # Мелким шрифтом
    activity = discord.Activity(
        type=discord.ActivityType.unknown,
        name=name,
        state=status_state
    )
    # Обновляем статус бота
    await bot.change_presence(activity=activity)