from bot_init import bot
from commands import (echo_command, gpt_command, help_command, ping_command,
                      user_role_command)
from commands.github import (achang_command, forks_command, github_processor,
                             milestones_command, review_command, pr_changelog_send)
from config import DISCORD_KEY
from events import on_message, on_ready, on_error, on_command

if __name__ == '__main__':
    bot.run(DISCORD_KEY)

#TODO: Add logging: @nixsilvam404