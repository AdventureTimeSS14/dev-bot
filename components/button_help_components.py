import disnake
from disnake.ui import Button

# Создание кнопок
button_help = Button(label="&help", style=disnake.ButtonStyle.green, custom_id="button_help_id")
button_team_help = Button(label="&team_help", style=disnake.ButtonStyle.blurple, custom_id="button_team_help_id")
button_git_help = Button(label="&git_help", style=disnake.ButtonStyle.gray, custom_id="button_git_help_id")
button_admin_help = Button(label="&admin_help", style=disnake.ButtonStyle.red, custom_id="button_admin_help_id")


action_row_button_help = disnake.ui.ActionRow(button_help, button_team_help, button_git_help, button_admin_help)