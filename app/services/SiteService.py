from app.db.repositories.SiteRepository import SiteRepository


class SiteService:
    def __init__(self, site_repo: SiteRepository):
        self.site_repo = site_repo

    async def create_site(self, user_id: str, url: str, interval: int):
        site = await self.site_repo.create_site(user_id=user_id, url=url, interval=interval)
        #TODO реализовать автоопрос