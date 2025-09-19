import asyncio
from datetime import datetime, timedelta
from typing import Optional

class BackgroundTask:
    def __init__(self):
        from app.monitoring.SiteChecker import SiteChecker
        from app.services.NotifyService import NotifyService
        from app.services.SiteService import SiteService
        self.sites_schedule = {}
        self.site_service: Optional[SiteService] = None
        self.notify_service: Optional[NotifyService] = None
        self.site_checker: Optional[SiteChecker] = None

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
                "next_check": now + timedelta(minutes=site.check_interval)
            }

    async def add_or_update_site(self, site):
        """Добавление нового сайта или обновление интервала существующего"""
        now = datetime.utcnow()
        self.sites_schedule[site.id] = {
            "site": site,
            "next_check": now + timedelta(minutes=site.check_interval)
        }
    async def delete_site(self, site):
        ...
    #TODO

    async def check_site(self, site):
        """Задача проверки сайта"""
        ...
        #TODO
        # await self.notify_service.send_msg(site)

    async def run(self):
        """Главный цикл проверки сайтов"""
        while True:
            now = datetime.utcnow()
            for site_id, info in list(self.sites_schedule.items()):
                if now >= info["next_check"]:
                    await self.check_site(info["site"])
                    info["next_check"] = now + timedelta(minutes=info["site"].check_interval)
            await asyncio.sleep(5)
