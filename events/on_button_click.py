import disnake


from bot_init import bot

from disnake.ui import Modal, TextInput

class BugReportModal(Modal):
    def __init__(self):
        # Создаем текстовое поле для ввода сообщения с custom_id
        text_input = TextInput(
            label="Подробности о сообщении", 
            placeholder="Опишите баг, отзыв или предложение...", 
            style=disnake.TextInputStyle.long,
            custom_id="bug_report_details"  # Уникальный custom_id для данного поля
        )
        
        # Инициализация модального окна с компонентом text_input
        super().__init__(title="🚨 Сообщение о баге/отзыв/предложение", components=[text_input])

    async def callback(self, inter: disnake.MessageInteraction):
        try:
            # Получаем введённый текст через text_inputs
            report_text = inter.text_values['bug_report_details']  # Доступ к текстовому полю

            # Указание канала для отправки сообщения
            target_channel_id = 1333381720996843551  # Замените на нужный ID канала
            target_channel = inter.bot.get_channel(target_channel_id)
            
            if target_channel:
                # Создаем Embed для отправки
                embed = disnake.Embed(
                    title="📝 Новый отзыв/баг-репорт",
                    description=f"Сообщение от пользователя {inter.author.mention} ({inter.author.id}):",
                    color=disnake.Color.green()
                )
                embed.add_field(name="Текст сообщения:", value=report_text, inline=False)
                embed.set_footer(text="Отправлено из личных сообщений")

                # Пересылаем сообщение в канал
                await target_channel.send(embed=embed)
            
            # Ответ пользователю с подтверждением
            await inter.response.send_message(
                "Спасибо за ваше сообщение! Мы внимательно его рассмотрим и постараемся улучшить сервис. 😊", 
                ephemeral=True
            )
        
        except Exception as e:
            # Логирование ошибки (если происходит ошибка)
            print(f"Произошла ошибка при отправке сообщения: {e}")
            try:
                await inter.response.send_message(
                    "Извините, произошла ошибка при обработке вашего сообщения. Пожалуйста, попробуйте снова позже.",
                    ephemeral=True
                )
            except Exception as inner_error:
                print(f"Ошибка при отправке сообщения об ошибке: {inner_error}")     
    
# async def isinstance_chat(message):
#     try:
#         # Если сообщение пришло в личные сообщения
#         if isinstance(message.channel, disnake.DMChannel):
#             # Если это не команда (не начинается с префикса)
#             if not message.content.startswith(bot.command_prefix):
#                 # Отправляем ответ на сообщение
#                 await message.channel.send(
#                     "Здравствуйте! Спасибо за ваше сообщение. "
#                     "Ваше предложение или баг-репорт отправлен техническому администратору. "
#                     "Мы будем стараться улучшать сервис и благодарны за ваш вклад! 😊"
#                 )
                
#                 # ID канала, куда нужно отправить сообщение
#                 target_channel_id = 1333381720996843551  # Замените на нужный канал
#                 # Получаем канал по ID
#                 target_channel = bot.get_channel(target_channel_id)
#                 if target_channel:
#                     embed = disnake.Embed(
#                         title="Новый отзыв/баг-репорт",
#                         description=f"Сообщение от пользователя {message.author.display_name} ({message.author.mention}) ({message.author.id}):",
#                         color=disnake.Color.yellow()
#                     )
#                     embed.add_field(
#                         name="Текст сообщения:",
#                         value=message.content,
#                         inline=False
#                     )
#                     embed.set_footer(
#                         text=f"Отправлено: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')} от {message.author.display_name}",
#                         icon_url=message.author.avatar.url
#                     )
#                     embed.set_author(
#                         name=message.author.display_name,
#                         icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
#                     )
#                     # Пересылаем сообщение в целевой канал
#                     await target_channel.send(embed=embed)
#                 else:
#                     print(f"Не удалось найти канал с ID {target_channel_id}")
#         return
#     except Exception as e:
#         # Логирование ошибки (можно заменить на логгер)
#         print(f"Ошибка при обработке сообщения в личных сообщениях: {e}")
#         # Можно отправить пользователю сообщение об ошибке
#         try:
#             await message.channel.send(
#                 "Извините, произошла ошибка при обработке "
#                 "вашего сообщения. Пожалуйста, попробуйте позже."
#             )
#         except Exception as inner_error:
#             print(f"Ошибка при отправке сообщения об ошибке: {inner_error}")


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
    
    if inter.component.custom_id == "button_bug_report_id":
        await inter.response.send_modal(BugReportModal())
