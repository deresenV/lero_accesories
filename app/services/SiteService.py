from app.db.models import Site
from app.db.repositories.SiteRepository import SiteRepository
from app.monitoring.BackgroundResponses import BackgroundResponses


class SiteService:
    def __init__(self, site_repo: SiteRepository, task_checker: BackgroundResponses, reporter):
        self.site_repo = site_repo
        self.task_checker = task_checker
        self.reporter = reporter


    async def create_site(self, user_id: str, url: str, interval: int):
        """Создать сайт и загрузить его в фоновые обработчики """
        site = await self.site_repo.create_site(user_id=user_id, url=url, interval=interval)

        await self.task_checker.add_or_update_site(site)
        await self.reporter.add_site(site)


    async def get_site_by_id(self, id:int) -> Site:
        """Получить сайт по его id"""
        site = await self.site_repo.get_site_by_id(id)
        return site

    async def edit_data(self, type: str, id: int, update_data: str) -> Site:
        """Редактирование данных в сайте(URL/interval)"""
        if type == "url":
            site = await self.site_repo.update_site_url(id,update_data)
            await self.task_checker.add_or_update_site(site)
        elif type == "interval":

            site = await self.site_repo.update_site_interval(id, int(update_data))
            await self.task_checker.add_or_update_site(site)

        return site

    async def delete_site(self, id: int) -> str:
        """Удаление сайта по его id"""
        site = await self.site_repo.delete_site(id)
        if site:
            await self.task_checker.delete_site(id)
            return "Сайт удален"
        return "При удалении сайта произошла ошибка"

    async def get_all_sites(self):
        """Получить все сайты"""
        return await self.site_repo.get_all_sites()