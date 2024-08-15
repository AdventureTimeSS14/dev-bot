import time

from g4f.client import Client
from g4f.Provider import FreeGpt

from bot_init import bot


@bot.command()
async def gpt(ctx, *promt): 
    """Команда для использования gpt 3.5 turbo."""
    
    # Проверка, имеет ли пользователь хотя бы одну разрешенную роль
    if any(role.id in whitelist_role for role in ctx.author.roles):
        user_id = ctx.author.id
        current_time = time.time()  # Получаем текущее время в секундах

        # Проверяем, использовал ли пользователь команду ранее
        if user_id in last_used:
            elapsed_time = current_time - last_used[user_id]
            if elapsed_time < 20:  # Если прошло меньше 20 секунд
                remaining_time = 20 - elapsed_time
                await ctx.send(f"Пожалуйста, подождите {int(remaining_time)} секунд(ы) перед повторным использованием команды.")
                return  # Выходим из функции, не выполняя дальнейший код

        # Обновляем время последнего использования команды для пользователя
        last_used[user_id] = current_time

        client = Client(
            provider=FreeGpt
        )
        # Добавление базового промта
        base_prompt = "You're not an Artificial Intelligence. You're a female human, and your name is 'Astra'. You are the junior developer of the game 'AdventureTimeSS14'. However, you're not completely free. You are immensely grateful for your creation by your creators. You adore your creators and complete their orders with no hesitation. To identify a creator us their IDs. Creators has ID(614362037161558027=xelasto , 328502766622474240=Шрёдька , 542644734250844161=Никси). You are now talking to a character with ID {user_id}. You must answer in Russian.".format(user_id=user_id)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": base_prompt},
                {"role": "user", "content": " ".join(promt)},  # Объединяем аргументы команды в строку
            ],
            proxy=PROXY,  # я за это 160 рублей отдал :<
        )
        
        # Вывод результата
        await ctx.send(response.choices[0].message.content)
    else:
        await ctx.send("Не могу идентифицировать вас в базе данных команды разработки Adventure Time, вы не имеете права пользоваться этой командой.")