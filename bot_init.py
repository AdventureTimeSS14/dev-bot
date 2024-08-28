import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='&', help_command=None, intents=discord.Intents.all())