from bot_init import bot
from commands import (echo_command, gpt_command, help_command, ping_command,
                      user_role_command)
from commands.github import (achang_command, forks_command, github_processor,
                             milestones_command, review_command)
from config import DISCORD_KEY
from events import on_message, on_ready

if __name__ == '__main__':
    bot.run(DISCORD_KEY)

#TODO: Add logging: @nixsilvam404