from app.db.models import Site


class SiteRepository:
    def __init__(self, session):
        self.session = session

    async def create_site(self, user_id: str, url: str, interval: int):
        site = Site(
            telegram_id_author = user_id,
            url = url,
            check_interval = interval
        )
        self.session.add(site)
        await self.session.commit()
        return site

    async def get_site_by_id(self, id: int):
        return await self.session.get(Site, id)

    async def update_site_url(self, site_id: int, new_url: str) -> Site | None:
        """Обновляет URL сайта"""
        site = await self.get_site_by_id(site_id)
        if site:
            site.url = new_url
            await self.session.commit()
        return site

    async def update_site_interval(self, site_id: int, new_interval: int) -> Site | None:
        """Обновляет интервал опроса сайта"""
        site = await self.get_site_by_id(site_id)
        if site:
            site.check_interval = new_interval
            await self.session.commit()
        return site

    async def delete_site(self, site_id: int) -> bool:
        """Удаляет сайт по id. Возвращает True если удалён, False если не найден"""
        site = await self.get_site_by_id(site_id)
        if site:
            await self.session.delete(site)
            await self.session.commit()
            return True
        return False