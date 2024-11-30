from bot_init import bot
import mariadb
import discord
from config import (USER, PASSWORD, HOST, PORT, DATABASE)

color = discord.Color.dark_purple()

@bot.command()
async def db_info(ctx):
    conn = None  # Инициализация переменной для соединения
    try:
        # Преобразование порта в целое число
        port = int(PORT)  # Убедитесь, что PORT - это целое число
        
        conn = mariadb.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=port,
            database=DATABASE
        )

        embed = discord.Embed(
            title="Информация о базе данных",
            color=color
        )
        embed.add_field(name="База данных", value=DATABASE)
        
        # Получаем информацию о сервере
        cur = conn.cursor()
        cur.execute("SELECT VERSION()")  # Запрос для получения версии сервера
        server_version = cur.fetchone()[0]
        embed.add_field(name="Статус сервера", value="Соединение открыто" if conn.open else "Соединение закрыто")
        embed.add_field(name="Информация о сервере", value=conn.server_info)
        embed.add_field(name="Версия сервера", value=conn.server_version)

        cur.execute("SHOW TABLES")
        tables = cur.fetchall()

        if not tables:
            embed.add_field(name="База данных пуста", value="В базе данных нет таблиц")
        else:
            embed.add_field(name="Список таблиц в базе данных:", value="\n".join([table[0] for table in tables]))

        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Ошибка: {e}")  # Вывод ошибки в консоль
        embed = discord.Embed(
            title="Ошибка",
            description=str(e),
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    finally:
        if conn:  # Проверка, было ли установлено соединение
            conn.close()