from bot_init import bot
from commands import (echo_command, gpt_command, help_command,
                      list_team_command, ping_command, user_role_command)
from commands.adt_team import (add_role_command, add_vacation_command,
                               new_team_command, remove_role_command,
                               remove_team_command, team_help_command,
                               tweak_team_command, end_vacation_command)
from commands.dbCommand import help_command, info_command, status_command
from commands.github import (achang_command, forks_command, github_processor,
                             milestones_command, pr_changelog_send,
                             review_command)
from config import DISCORD_KEY
from events import on_command, on_error, on_message, on_ready

if __name__ == '__main__':
    bot.run(DISCORD_KEY)

#TODO: Add logging: @nixsilvam404