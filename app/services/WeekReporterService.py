import asyncio
from datetime import timedelta, datetime

from app.services.LogsService import LogsService
from app.services.NotifyService import NotifyService


class WeekReporter:
    def __init__(self, site_service, logs_service: LogsService, notify_service: NotifyService):
        self.site_service = site_service
        self.logs_service = logs_service
        self.notify_service = notify_service

        self.week = 7
        self.sites_schedule = {}


    async def load_sites(self):
        """Загрузка сайтов через сервис"""
        now = datetime.utcnow()
        sites = await self.site_service.get_all_sites()
        for site in sites:
            self.sites_schedule[site.id] = {
                "site": site,
                "next_check": now + timedelta(days=7)
            }


    async def add_site(self, site):
        """Добавление нового сайта"""
        now = datetime.utcnow()
        self.sites_schedule[site.id] = {
            "site": site,
            "next_check": now + timedelta(days=7)
        }


    async def delete_site(self, site_id: int):
        """Удаляем сайт из расписания безопасно"""
        if site_id in self.sites_schedule:
            self.sites_schedule.pop(site_id)


    async def processing_report(self, site):
        """Обработка данных и отправка"""
        uptime, downtime, total = await self.logs_service.get_week_ago_statistics(site.id, site.telegram_id_author)
        message = f"Статистика сайта за неделю:\nUptime: {uptime}%\nDowntime: {downtime}%\nВсего проверок: {total}"
        await self.notify_service.send_message(site.telegram_id_author, message)


    async def run(self):
        """Главный цикл еженедельного репортера"""
        while True:
            now = datetime.utcnow()
            for site_id, info in list(self.sites_schedule.items()):
                if now >= info["next_check"]:
                    await self.processing_report(info["site"])
                    info["next_check"] = now + timedelta(days=7)
            await asyncio.sleep(5)