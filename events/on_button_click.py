import disnake


from bot_init import bot


@bot.event
async def on_button_click(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "button_help_id":
        await bot.get_command("help").callback(inter)

    if inter.component.custom_id == "button_team_help_id":
        await bot.get_command("team_help").callback(inter)

    if inter.component.custom_id == "button_git_help_id":
        await bot.get_command("git_help").callback(inter)

    if inter.component.custom_id == "button_admin_help_id":
        await bot.get_command("admin_help").callback(inter)

        