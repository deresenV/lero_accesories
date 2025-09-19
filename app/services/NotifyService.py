class NotifyService:
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, site, message):
        await self.bot.send_message(chat_id=int(site.telegram_id_author),text=message)