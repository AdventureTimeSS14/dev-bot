import requests
import disnake

from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from commands.post_admin.utils import get_field_value

from config import (
    WHITELIST_ROLE_ID_ADMINISTRATION_POST,
    ADDRESS_MRP,
    POST_ADMIN_HEADERS
)


@bot.command()
@has_any_role_by_id(WHITELIST_ROLE_ID_ADMINISTRATION_POST)
async def admin_info(ctx):
    """
    Команда для получения информации о текущем состоянии администраторского интерфейса.
    Включает данные о текущей игре, игроках, настроенных правилах и других параметрах.
    """
    
    url = f"http://{ADDRESS_MRP}:1212/admin/info"
    
    response = requests.get(url, headers=POST_ADMIN_HEADERS)
    
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
