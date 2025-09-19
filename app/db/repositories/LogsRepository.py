from sqlalchemy import select

from app.db.models import Log


class LogsRepository:
    def __init__(self, session):
        self.session = session

    async def create_log(self, site, status_code, response_time):
        log = Log(
            author_id = site.telegram_id_author,
            site_id = site.id,
            status_code = status_code,
            response_time_ms = response_time
        )
        self.session.add(log)
        await self.session.commit()

    async def get_all_log_by_user_site(self, user_id, site_id):
        site_logs = select(Log).where(
Log.site_id == site_id,
            Log.author_id == user_id
        )
        result = await self.session.execute(site_logs)
        return result.scalars().all()

