"""
Этот модуль инициализирует бота для работы с Discord.
Настроены необходимые параметры для запуска и обработки команд.
"""

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='&', help_command=None, intents=discord.Intents.all())
