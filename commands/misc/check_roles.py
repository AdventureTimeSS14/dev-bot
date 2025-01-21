from disnake.ext import commands


def has_any_role_by_id(*role_id_groups):
    """
    Декоратор для проверки, имеет ли пользователь одну из указанных ролей из нескольких групп ролей.

    :param role_id_groups: Список массивов ID ролей, доступ к которым проверяется.
    :return: Декоратор команды.
    """
    async def predicate(ctx):
        # Проверяем, есть ли у пользователя хотя бы одна роль из каждого массива ролей
        has_role = False
        for role_ids in role_id_groups:
            if any(role.id in role_ids for role in ctx.author.roles):
                has_role = True
                break  # Прерываем, как только нашли хотя бы одну подходящую роль
        if not has_role:
            await ctx.send("❌ У вас нет доступа к этой команде.")
        return has_role

    return commands.check(predicate)
