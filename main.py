import discord
from discord.ext import commands
from discord.ui import View, Button

intents = discord.Intents.default()
intents.members = True  # Нужно для работы с ролями

bot = commands.Bot(command_prefix="?", intents=intents)

TOKEN = "MTM1OTE0MTQyOTY3ODU3NTY5Ng.GK5S2L.tIf-ASS5pa2-QmtffwZUx9u1eZRytcbdn24LYw"
CHANNEL_ID = 1359121463436775540
ROLE_ID = 1359121462903963687


class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Пройти верификацию ✅", style=discord.ButtonStyle.success, custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(ROLE_ID)
        if role is None:
            await interaction.response.send_message(
                "⚠️ Роль не найдена. Обратитесь к vexar_ofc", ephemeral=True
            )
            return

        if role in interaction.user.roles:
            await interaction.response.send_message(
                "✅ Вы уже прошли верификацию!", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role, reason="Прошел верификацию")

            try:
                await interaction.user.send("🎉 Вы успешно прошли верификацию и получили доступ к серверу!")
            except discord.Forbidden:
                await interaction.response.send_message(
                    "🎉 Вы успешно прошли верификацию и получили доступ к серверу!",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "📬 Проверьте свои личные сообщения!",
                    ephemeral=True
                )


@bot.event
async def on_ready():
    print(f"Бот {bot.user} запущен!")

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Канал не найден.")
        return

    view = VerifyButton()
    verification_text = (
        "✨ Для обеспечения безопасности и комфорта нашего сервера, "
        "нажмите на кнопку ниже, чтобы пройти верификацию и получить роль."
    )

    # Ищем сообщение от бота с нужной кнопкой
    async for message in channel.history(limit=50):
        if message.author == bot.user and message.components:
            for row in message.components:
                for item in row.children:
                    if isinstance(item, discord.ui.Button) and item.custom_id == "verify_button":
                        await message.edit(content=verification_text, view=view)
                        print("♻️ Сообщение с кнопкой обновлено.")
                        return

    # Если не найдено — создаём новое
    await channel.send(verification_text, view=view)
    print("✅ Новое сообщение с кнопкой отправлено.")

bot.run(TOKEN)
