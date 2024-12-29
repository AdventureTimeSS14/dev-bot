from discord.ext import commands


def has_any_role_by_id(role_ids):
    """
    Декоратор для проверки, имеет ли пользователь одну из указанных ролей по их ID.

    :param role_ids: Список ID ролей, доступ к которым проверяется.
    :return: Декоратор команды.
    """

    async def predicate(ctx):
        # Проверяем наличие хотя бы одной из указанных ролей у пользователя
        has_role = any(role.id in role_ids for role in ctx.author.roles)
        if not has_role:
            await ctx.send("❌ У вас нет доступа к этой команде.")
        return has_role

    return commands.check(predicate)
