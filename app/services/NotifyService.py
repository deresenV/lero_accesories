class NotifyService:
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, chat_id, message):
        await self.bot.send_message(chat_id=chat_id,text=message)