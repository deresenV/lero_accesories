import pytest
from datetime import datetime, timedelta
from app.db.models import Log

class DummySite:
    """Простой объект-заглушка для имитации Site"""
    def __init__(self, id, telegram_id_author):
        self.id = id
        self.telegram_id_author = telegram_id_author

@pytest.mark.asyncio
async def test_create_and_get_logs(logs_repo, session):
    site = DummySite(id=1, telegram_id_author=12345)

    await logs_repo.create_log(site, status_code=200, response_time=123.4)
    logs = await logs_repo.get_all_log_by_user_site(user_id=12345, site_id=1)

    assert len(logs) == 1
    assert logs[0].status_code == 200
    assert logs[0].response_time_ms == 123.4

@pytest.mark.asyncio
async def test_get_time_ago_logs(logs_repo, session):
    site = DummySite(id=2, telegram_id_author=999)

    old_log = Log(
        author_id=site.telegram_id_author,
        site_id=site.id,
        status_code=500,
        response_time_ms=200,
        timestamp=datetime.utcnow() - timedelta(days=10)
    )
    new_log = Log(
        author_id=site.telegram_id_author,
        site_id=site.id,
        status_code=200,
        response_time_ms=100,
        timestamp=datetime.utcnow() - timedelta(days=1)
    )
    session.add_all([old_log, new_log])
    await session.commit()

    week_ago = datetime.utcnow() - timedelta(days=7)
    logs = await logs_repo.get_time_ago_logs_for_site(
        time_ago=week_ago,
        site_id=site.id,
        user_id=site.telegram_id_author
    )

    assert len(logs) == 1
    assert logs[0].status_code == 200
