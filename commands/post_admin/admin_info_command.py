import json
import requests
import disnake
from disnake.ext import commands
from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id

from config import (
    WHITELIST_ROLE_ID_ADMINISTRATION_POST,
    POST_ADMIN_API,
    POST_ADMIN_GUID,
    POST_ADMIN_NAME,
    ACTOR_DATA_ADMIN,
    ADDRESS_MRP,
    HEAD_ADT_TEAM
)

actor_data = {
    "Guid": str(POST_ADMIN_GUID),
    "Name": str(POST_ADMIN_NAME)
}

headers = {
    "Authorization": f"SS14Token {POST_ADMIN_API}",
    "Content-Type": "application/json",
    "Actor": json.dumps(actor_data)
}

def get_field_value(data, keys, default="Не задано"):
    """
    Функция для безопасного извлечения значения из вложенной структуры данных.
    Если значение не найдено, возвращается default.
    """
    try:
        for key in keys:
            data = data.get(key, {})
            if not data:
                return default
        return data if data else default
    except Exception as e:
        print(f"Ошибка извлечения данных: {e}")
        return default

@bot.command()
@has_any_role_by_id(HEAD_ADT_TEAM)
async def bunker(ctx, toggle: str):
    # Устанавливаем адрес URL
    url = f"http://{ADDRESS_MRP}:1212/admin/actions/panic_bunker"
    
    # Проверяем, что toggle имеет корректное значение
    if toggle.lower() not in ["true", "false"]:
        await ctx.send("Ошибка: пожалуйста, используйте 'true' или 'false' для включения/выключения бункера.")
        return
    
    # Определяем значение для бункера
    bunker_bool = True if toggle.lower() == "true" else False
    
    # Подготовка данных для запроса
    data = {
        "game.panic_bunker.enabled": bunker_bool,
    }
    
    try:
        # Отправка PATCH запроса
        response = requests.patch(url, headers=headers, json=data)
        
        # Проверяем статус ответа
        if response.status_code == 200:
            status = "включен" if bunker_bool else "выключен"
            await ctx.send(f"Паник-бункер успешно {status}.")
        else:
            await ctx.send(f"Ошибка при изменении состояния паник-бункера. Код ошибки: {response.status_code}.")
            print(f"Error: {response.status_code}, {response.text}")
    
    except requests.exceptions.RequestException as e:
        # Обработка ошибок сети
        await ctx.send(f"Произошла ошибка при отправке запроса: {str(e)}")
        print(f"Request error: {str(e)}")


@bot.command()
@has_any_role_by_id(WHITELIST_ROLE_ID_ADMINISTRATION_POST)
async def admin_info(ctx):
    """
    Команда для получения информации о текущем состоянии администраторского интерфейса.
    Включает данные о текущей игре, игроках, настроенных правилах и других параметрах.
    """
    
    url = f"http://{ADDRESS_MRP}:1212/admin/info"
    
    response = requests.get(url, headers=headers)
    
    # Логируем полный ответ для отладки
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Обработка ответа
    if response.status_code == 200:
        data = response.json()
        
        # # Логируем данные, чтобы понять их структуру
        # print(f"Response JSON Data: {json.dumps(data, indent=4)}")
        
        # Создание Embed для красивого вывода
        embed = disnake.Embed(
            title="Информация о сервере SS14",
            description="Данная команда выводит информацию о текущем состоянии сервера Mrp в подробном виде SS14.",
            color=disnake.Color.blue()
        )
        
        # Основные данные
        embed.add_field(name="ID Раунда", value=get_field_value(data, ["RoundId"]), inline=False)
        embed.add_field(name="Название карты", value=get_field_value(data, ["Map", "Name"]), inline=False)
        embed.add_field(name="MOTD (Сообщение дня)", value=get_field_value(data, ["MOTD"], default="Нет сообщения"), inline=False)
        embed.add_field(name="Геймпресет", value=get_field_value(data, ["GamePreset"]), inline=False)
        
        # Список игроков
        players = data.get("Players", [])
        if players:
            # Разделение списка игроков на несколько частей, если их слишком много
            players_list = "\n".join([f"**{player['Name']}** - {'Админ' if player['IsAdmin'] else 'Игрок'}" for player in players if not player['IsDeadminned']])
            deadminned_list = "\n".join([f"**{player['Name']}** - {('Админ' if player['IsAdmin'] else 'Игрок')} (Deadminned)" for player in players if player['IsDeadminned']])
            
            # Если список игроков слишком длинный, разбиваем его на несколько полей
            def split_text(text, max_length=1024):
                """Функция для разделения текста на части, чтобы не превышать лимит символов."""
                chunks = []
                while len(text) > max_length:
                    split_idx = text.rfind("\n", 0, max_length)  # Разделить по последнему \n, чтобы не обрывать слово
                    chunks.append(text[:split_idx])
                    text = text[split_idx + 1:]
                chunks.append(text)  # Остаток
                return chunks

            # Разделяем списки игроков и деадминов на части
            player_chunks = split_text(players_list)
            deadminned_chunks = split_text(deadminned_list)

            # Добавляем все части в Embed, если текст был разбит
            for i, chunk in enumerate(player_chunks):
                embed.add_field(name=f"Игроки на сервере" if i == 0 else f"Игроки на сервере (часть {i+1})", value=chunk, inline=False)
            for i, chunk in enumerate(deadminned_chunks):
                embed.add_field(name=f"Игроки в деадмине" if i == 0 else f"Игроки в деадмине (часть {i+1})", value=chunk, inline=False)
        else:
            embed.add_field(name="Игроки на сервере", value="Нет игроков", inline=False)
            embed.add_field(name="Игроки в деадмине", value="Нет игроков в деадмине", inline=False)

        # Правила игры
        game_rules = get_field_value(data, ["GameRules"], default="Нет доступных правил")
        
        # Разбиение списка правил на части, если он слишком длинный
        game_rules_list = "\n".join(game_rules) if isinstance(game_rules, list) else game_rules
        game_rules_chunks = split_text(game_rules_list)

        # Добавляем части в Embed
        for i, chunk in enumerate(game_rules_chunks):
            embed.add_field(name=f"Правила игры" if i == 0 else f"Правила игры (часть {i+1})", value=chunk, inline=False)

        # Паника
        panic_bunker_info = data.get("PanicBunker", {})
        if panic_bunker_info:
            panic_info = "\n".join([f"{key}: {value}" for key, value in panic_bunker_info.items() if value is not None])
            panic_status = panic_info if panic_info else "Не активирован"
        else:
            panic_status = "Не активирован"
        
        embed.add_field(name="Panic Bunker", value=panic_status, inline=False)
        
        # Отправка Embed в канал
        await ctx.send(embed=embed)
        
    else:
        # Если запрос не успешен
        await ctx.send(f"Ошибка запроса: {response.status_code}, {response.text}")

        
@bot.command()
@has_any_role_by_id(WHITELIST_ROLE_ID_ADMINISTRATION_POST)
async def game_rules(ctx):
    """
    Команда для получения информации о текущих правилах игры.
    Включает список доступных игровых правил на сервере SS14.
    """
    
    url = f"http://{ADDRESS_MRP}:1212/admin/game_rules"  # Измените на актуальный endpoint
    
    response = requests.get(url, headers=headers)
    
    # # Логируем полный ответ для отладки
    # print(f"Response Status Code: {response.status_code}")
    # print(f"Response Text: {response.text}")
    
    # Обработка ответа
    if response.status_code == 200:
        data = response.json()
        
        # # Логируем данные, чтобы понять их структуру
        # print(f"Response JSON Data: {json.dumps(data, indent=4)}")
        
        # Создание Embed для красивого вывода
        embed = disnake.Embed(
            title="Игровые правила сервера SS14",
            description="Данная команда выводит список правил на сервере.",
            color=disnake.Color.green()
        )
        
        # Получаем список правил
        game_rules = get_field_value(data, ["GameRules"], default=[])
        
        # Разбиение списка на несколько частей, если он слишком длинный
        chunk_size = 10  # Максимальное количество правил в одном поле
        for i in range(0, len(game_rules), chunk_size):
            chunk = "\n".join(game_rules[i:i + chunk_size])
            embed.add_field(name=f"Правила (часть {i // chunk_size + 1})", value=chunk, inline=False)
        
        # Отправка Embed в канал
        await ctx.send(embed=embed)
        
    else:
        # Если запрос не успешен
        await ctx.send(f"Ошибка запроса: {response.status_code}, {response.text}")
        
        
@bot.command()
@has_any_role_by_id(WHITELIST_ROLE_ID_ADMINISTRATION_POST)
async def admin_presets(ctx):
    """
    Команда для получения информации о доступных геймпресетах.
    Включает список всех доступных пресетов и их описание.
    """
    
    url = f"http://{ADDRESS_MRP}:1212/admin/presets"
    
    response = requests.get(url, headers=headers)
    
    # # Логируем полный ответ для отладки
    # print(f"Response Status Code: {response.status_code}")
    # print(f"Response Text: {response.text}")
    
    # Обработка ответа
    if response.status_code == 200:
        data = response.json()

        # # Логируем структуру данных для отладки
        # print(f"Response JSON Data: {json.dumps(data, indent=4)}")
        
        # Создание Embed для красивого вывода
        embed = disnake.Embed(
            title="Доступные Геймпресеты",
            description="Данная команда выводит информацию о всех доступных геймпресетах на сервере.",
            color=disnake.Color.blue()
        )

        # Список пресетов
        presets = data.get("Presets", [])

        if presets:
            presets_list = []
            for preset in presets:
                # # Логируем каждый пресет
                # print(f"Preset Data: {json.dumps(preset, indent=4)}")

                # Получаем название и описание, если они существуют
                name = preset.get('ModeTitle', 'Без названия')
                description = preset.get('Description', 'Описание отсутствует')
                preset_id = preset.get('Id', 'Без ID')

                presets_list.append(f"**{name}** (ID: {preset_id}): {description}")

            # Разделение текста на части, если нужно
            def split_text(text, max_length=1024):
                """Функция для разделения текста на части, чтобы не превышать лимит символов."""
                chunks = []
                while len(text) > max_length:
                    split_idx = text.rfind("\n", 0, max_length)  # Разделить по последнему \n, чтобы не обрывать слово
                    chunks.append(text[:split_idx])
                    text = text[split_idx + 1:]
                chunks.append(text)  # Остаток
                return chunks

            # Разделяем список пресетов на части
            preset_chunks = split_text("\n".join(presets_list))

            # Добавляем все части в Embed
            for i, chunk in enumerate(preset_chunks):
                embed.add_field(name=f"Геймпресеты" if i == 0 else f"Геймпресеты (часть {i+1})", value=chunk, inline=False)
        else:
            embed.add_field(name="Геймпресеты", value="Нет доступных пресетов", inline=False)

        # Отправка Embed в канал
        await ctx.send(embed=embed)

    else:
        # Если запрос не успешен
        await ctx.send(f"Ошибка запроса: {response.status_code}, {response.text}")
