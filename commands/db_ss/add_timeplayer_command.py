import disnake
import sqlite3
from bot_init import bot
from config import (
    WHITELIST_ROLE_ID_ADMINISTRATION_POST,
)
from datetime import timedelta  # Импортируем timedelta
from commands.misc.check_roles import has_any_role_by_id

# Параметры подключения для LiteSQL
DB_PARAMS = {
    'database': "C:/Develop/ss14/space_station_ADT/bin/Content.Server/data/preferences.db"
}

# Команда для добавления или вычитания времени для трекера игрока
@bot.command()
@has_any_role_by_id(WHITELIST_ROLE_ID_ADMINISTRATION_POST)
async def add_timeplayer(ctx, user_name: str, tracker_name: str, minutes: int):
    # Проверка на запрещенного пользователя
    forbidden_user_id = "725633890726838282"  # ID пользователя, которому запрещен доступ
    if str(ctx.author.id) == forbidden_user_id:
        await ctx.send('У вас нет доступа к этой информации.')
        return

    try:
        # Подключение к базе данных
        connection = sqlite3.connect(DB_PARAMS['database'])
        cursor = connection.cursor()

        # Получаем user_id игрока по его никнейму
        cursor.execute('''SELECT user_id FROM player WHERE last_seen_user_name = ?;''', (user_name,))
        player_result = cursor.fetchone()

        if not player_result:
            await ctx.send(f'Игрок с ником {user_name} не найден.')
            return

        player_id = player_result[0]

        # Проверяем, существует ли трекер для этого игрока
        cursor.execute('''SELECT play_time_id, time_spent FROM play_time WHERE player_id = ? AND tracker = ?;''', (player_id, tracker_name))
        result = cursor.fetchone()

        # Формируем timedelta для прибавления/вычитания времени
        time_delta = timedelta(minutes=minutes)

        if result:
            # Если трекер найден, обновляем время
            play_time_id, time_spent = result

            # Разбираем строку времени (формат 00:26:45.335824)
            if isinstance(time_spent, str):
                try:
                    # Разбиваем строку на компоненты: часы, минуты, секунды и дробные секунды
                    time_parts = time_spent.split(":")
                    hours = int(time_parts[0])  # Часы
                    minutes = int(time_parts[1])  # Минуты
                    seconds_and_fraction = time_parts[2].split(".")
                    seconds = int(seconds_and_fraction[0])  # Секунды
                    fraction = float("0." + seconds_and_fraction[1])  # Дробная часть секунд

                    # Переводим всё в секунды
                    total_seconds = (hours * 3600) + (minutes * 60) + seconds + fraction

                    # Добавляем новые секунды
                    new_total_seconds = total_seconds + time_delta.total_seconds()

                    # Переводим обратно в формат
                    new_hours = int(new_total_seconds // 3600)
                    new_total_seconds %= 3600
                    new_minutes = int(new_total_seconds // 60)
                    new_seconds = int(new_total_seconds % 60)
                    new_fraction = new_total_seconds % 1  # Дробная часть

                    # Формируем строку времени в формате HH:MM:SS.ffffff (исправляем ошибку с лишней точкой)
                    new_time_str = f"{new_hours:02}:{new_minutes:02}:{new_seconds:02}.{new_fraction:.6f}".rstrip('0').rstrip('.')

                except Exception as e:
                    await ctx.send(f"Произошла ошибка при разборе времени: {e}")
                    print(f"Ошибка при разборе времени: {e}")
                    return
            else:
                new_time_str = str(time_delta)

            # Обновляем значение времени в базе данных
            cursor.execute('''UPDATE play_time SET time_spent = ? WHERE play_time_id = ?;''', (new_time_str, play_time_id))

            await ctx.send(f'Время на трекере {tracker_name} для игрока {user_name} было обновлено на {minutes} минут.')

        else:
            # Если трекер не найден, создаём новый
            total_seconds = int(time_delta.total_seconds())
            new_hours = total_seconds // 3600
            total_seconds %= 3600
            new_minutes = total_seconds // 60
            new_seconds = total_seconds % 60
            new_fraction = time_delta.total_seconds() % 1  # Дробная часть

            new_time_str = f"{new_hours:02}:{new_minutes:02}:{new_seconds:02}.{new_fraction:.6f}".rstrip('0').rstrip('.')

            cursor.execute('''INSERT INTO play_time (player_id, tracker, time_spent) VALUES (?, ?, ?);''', (player_id, tracker_name, new_time_str))

            await ctx.send(f'Трекер {tracker_name} был создан для игрока {user_name} и ему добавлено {minutes} минут.')

        # Сохраняем изменения
        connection.commit()

        # Закрытие соединения
        cursor.close()
        connection.close()

    except Exception as e:
        await ctx.send(f"Произошла ошибка при изменении времени: {e}")
        print(f"Ошибка: {e}")
