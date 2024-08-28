import discord
from discord.ext import commands


def has_any_role_by_id(role_ids):
    def predicate(ctx):
        return any(discord.utils.get(ctx.author.roles, id=role_id) for role_id in role_ids)
    return commands.check(predicate)