from app.db.repositories.LogsRepository import LogsRepository


class LogsService:
    def __init__(self, logs_repo: LogsRepository):
        self.logs_repo = logs_repo

    async def create_site_log(self, site, status_code, response_time):
        await self.logs_repo.create_log(site, status_code, response_time)


    async def get_all_log_by_user_site(self, user_id, site_id):
        return await self.logs_repo.get_all_log_by_user_site(user_id, site_id)