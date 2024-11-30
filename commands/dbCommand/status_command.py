import discord
import mariadb

from bot_init import bot
from config import DATABASE, HOST, PASSWORD, PORT, USER


@bot.command()
async def db_status(ctx):
    conn = None
    try:
        port = int(PORT)
        
        conn = mariadb.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=port,
            database=DATABASE
        )

        # Создаем красивый embed
        embed = discord.Embed(
            title="Статус БД",
            description="Успешно подключено к базе данных MariaDB!",
            color=discord.Color.dark_purple()
        )

        embed.add_field(name="Статус сервера", value="Соединение открыто" if conn.open else "Соединение закрыто")

        await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="Ошибка подключения",
            description=f"Не удалось подключиться к базе данных: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    finally:
        if conn:  # Проверяем, было ли установлено соединение перед закрытием
            conn.close()