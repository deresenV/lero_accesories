from aiogram import Bot


class NotifyService:
    def __init__(self, bot: Bot):
        self.bot = bot


    async def send_msg(self, site):
        await self.bot.send_message(chat_id=int(site.telegram_id_author),text=f"Проверен {site.url}")