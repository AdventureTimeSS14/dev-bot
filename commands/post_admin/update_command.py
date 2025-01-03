from bot_init import bot
from commands.misc.check_roles import has_any_role_by_id
from commands.post_admin.utils import send_server_request
from config import (
    SERVER_ADMIN_POST,
    POST_DATA_DEV,
    POST_DATA_MRP,
    POST_HEADERS_DEV,
    POST_HEADERS_MPR,
    ADDRESS_DEV,
    ADDRESS_MRP
)


@bot.command(name="update")
@has_any_role_by_id(SERVER_ADMIN_POST)
async def update(ctx, server_name: str):
    """
    Команда для обновления MRP или DEV сервера.
    Доступна только для пользователей с ролью из SERVER_ADMIN_POST.
    """
    url_mrp = f"http://{ADDRESS_MRP}:5000/instances/MRP/update"
    url_dev = f"http://{ADDRESS_DEV}:5000/instances/DEV/update"
    
    # Проверка корректности имени сервера
    if server_name.lower() not in ["mrp", "dev"]:
        await ctx.send("❌ Некорректное имя сервера. Используйте 'mrp' или 'dev'.")
        return
    
    # В зависимости от выбора сервера отправляем нужный запрос
    if server_name.lower() == "mrp":
        url = url_mrp
        data = POST_DATA_MRP
        headers = POST_HEADERS_MPR
    else:  # server_name.lower() == "dev"
        url = url_dev
        data = POST_DATA_DEV
        headers = POST_HEADERS_DEV
    
    # Уведомляем пользователя о начале операции
    await ctx.send(f"🔄 Запущен протокол обновления {server_name.upper()} сервера. Пожалуйста, подождите...")
    
    # Отправляем асинхронный запрос
    success, message = await send_server_request(ctx, url, data, headers)
    
    if success:
        await ctx.send(f"✅ Запрос к серверу {server_name.upper()} успешно отправлен.")
    else:
        await ctx.send(f"❌ Ошибка при отправке запроса к серверу {server_name.upper()}: {message}")
