from aiogram.types import BufferedInputFile
import pytz
from datetime import datetime, timedelta

from app.db.repositories.LogsRepository import LogsRepository


class LogsService:
    def __init__(self, logs_repo: LogsRepository):
        self.logs_repo = logs_repo

    async def create_site_log(self, site, status_code, response_time):
        """Создает лог для сайта пользователя"""
        await self.logs_repo.create_log(site, status_code, response_time)


    async def format_time_for_moscow(self, time):
        moscow_tz = pytz.timezone("Europe/Moscow")

        local_dt = time.replace(tzinfo=pytz.utc).astimezone(moscow_tz)
        formatted_time = local_dt.strftime("%d.%m.%y %H:%M")
        return formatted_time


    async def get_all_log_by_user_site(self, user_id, site_id):
        """Преобразует и отдает логи для сайта пользователя"""
        site_logs = await self.logs_repo.get_all_log_by_user_site(user_id, site_id)

        text_log = []
        for log in site_logs:
            formatted_time =  await self.format_time_for_moscow(log.timestamp)
            try:
                text_log.append(
                    f"Время: {formatted_time} | "
                    f"Статус: {log.status_code} | "
                    f"Время ответа: {round(log.response_time_ms, 2)} ms"
                )
            except TypeError:
                text_log.append(
                    f"Время: {formatted_time} | "
                    f"Статус: Нет ответа "
                )
        return text_log

    async def format_log_for_file(self, user_id: int, site_id: int):
        """Форматирование лога в файл"""
        text_log = await self.get_all_log_by_user_site(user_id, site_id)

        history_text = "История опроса сайта:\n\n" + "\n".join(text_log)
        file = BufferedInputFile(
            history_text.encode("utf-8"),  # переводим строку в байты
            filename=f"site_{site_id}_logs.txt"
        )

        return file

    async def _get_statistic(self, site_logs):
        if not site_logs:
            return {"uptime": 0, "downtime": 0, "total_checks": 0}

        total = len(site_logs)
        success = sum(1 for log in site_logs if log.status_code and log.status_code < 400)
        failed = total - success

        uptime = round(success / total * 100, 2)
        downtime = round(failed / total * 100, 2)

        return uptime, downtime, total


    async def get_all_statistic(self, user_id, site_id):
        """Получение и преобразование статистики сайта пользователя"""
        site_logs = await self.logs_repo.get_all_log_by_user_site(user_id, site_id)
        return await self._get_statistic(site_logs)


    async def get_week_ago_statistics(self, site_id, user_id):
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        logs = await self.logs_repo.get_time_ago_logs_for_site(week_ago, site_id, user_id)
        return await self._get_statistic(logs)