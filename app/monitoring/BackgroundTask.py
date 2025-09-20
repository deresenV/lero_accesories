import asyncio
from datetime import datetime, timedelta
from typing import Optional

from app.services.LogsService import LogsService


class BackgroundTask:
    def __init__(self):
        from app.monitoring.SiteChecker import SiteChecker
        from app.services.NotifyService import NotifyService
        from app.services.SiteService import SiteService

        self.sites_schedule = {}

        self.site_service: Optional[SiteService] = None
        self.notify_service: Optional[NotifyService] = None
        self.site_checker: Optional[SiteChecker] = None
        self.logs_service: Optional[LogsService] = None

    def set_service(self, service):
        """Передаём SiteService для работы с БД и уведомлений"""
        self.site_service = service

    async def load_sites(self):
        """Загрузка сайтов через сервис"""
        now = datetime.utcnow()
        sites = await self.site_service.get_all_sites()
        for site in sites:
            self.sites_schedule[site.id] = {
                "site": site,
                "last_response": None,
                "next_check": now + timedelta(minutes=site.check_interval)
            }


    async def add_or_update_site(self, site, last_response = None):
        """Добавление нового сайта или обновление интервала существующего"""
        now = datetime.utcnow()
        self.sites_schedule[site.id] = {
            "site": site,
            "last_response": last_response,
            "next_check": now + timedelta(minutes=site.check_interval)
        }

    async def delete_site(self, site_id: int):
        """Удаляем сайт из расписания безопасно"""
        if site_id in self.sites_schedule:
            self.sites_schedule.pop(site_id)


    async def processing_site(self, site, last_response):
        """Обработка сайта"""
        status_code, response_time, content = await self.site_checker.check_site(site.url)
        if not status_code:
            if last_response != "error":
                await self.notify_service.send_message(site.telegram_id_author, f"Возникла ошибка при обработке {site.url}.\nПроверьте правильность URL адресса")
                await self.add_or_update_site(site, "error")

        elif status_code>=400:
            if last_response != "error":
                await self.notify_service.send_message(site.telegram_id_author, f"Сайт: {site.url}\nВернул: {status_code} код.")
                await self.add_or_update_site(site, "error")

        else:
            if last_response:
                await self.add_or_update_site(site, None)
                await self.notify_service.send_message(site.telegram_id_author, f"Сайт {site.url} стал вновь доступен!")

        await self.logs_service.create_site_log(site, status_code, response_time)


    async def run(self):
        """Главный цикл проверки сайтов"""
        while True:
            now = datetime.utcnow()
            for site_id, info in list(self.sites_schedule.items()):
                if now >= info["next_check"]:
                    await self.processing_site(info["site"], info["last_response"])
                    info["next_check"] = now + timedelta(minutes=info["site"].check_interval)
            await asyncio.sleep(5)
