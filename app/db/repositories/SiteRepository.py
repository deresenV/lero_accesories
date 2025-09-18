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