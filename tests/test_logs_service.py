import pytest
from datetime import datetime, timedelta, timezone
from app.db.models import Log
from app.services.LogsService import LogsService


class DummySite:
    def __init__(self, id, telegram_id_author):
        self.id = id
        self.telegram_id_author = telegram_id_author


@pytest.mark.asyncio
async def test_create_site_log(logs_repo):
    service = LogsService(logs_repo)
    site = DummySite(1, 123)

    await service.create_site_log(site, 200, 150)
    logs = await logs_repo.get_all_log_by_user_site(site.telegram_id_author, site.id)

    assert len(logs) == 1
    assert logs[0].status_code == 200
    assert logs[0].response_time_ms == 150


@pytest.mark.asyncio
async def test_format_time_for_moscow():
    from pytz import timezone as tz
    service = LogsService(None)
    utc_time = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)

    formatted = await service.format_time_for_moscow(utc_time)
    moscow_tz = tz("Europe/Moscow")
    expected = utc_time.astimezone(moscow_tz).strftime("%d.%m.%y %H:%M")

    assert formatted == expected


@pytest.mark.asyncio
async def test_get_all_log_by_user_site(logs_repo):
    service = LogsService(logs_repo)
    site = DummySite(2, 456)

    await logs_repo.create_log(site, 200, 120)
    await logs_repo.create_log(site, 500, 300)

    text_logs = await service.get_all_log_by_user_site(site.telegram_id_author, site.id)

    assert len(text_logs) == 2
    assert "Статус: 200" in text_logs[0] or "Статус: 200" in text_logs[1]
    assert "Статус: 500" in text_logs[0] or "Статус: 500" in text_logs[1]


@pytest.mark.asyncio
async def test_site_stats_graphic(tmp_path, logs_repo):
    service = LogsService(logs_repo)
    site = DummySite(4, 999)

    await logs_repo.create_log(site, 200, 100)
    await logs_repo.create_log(site, 500, 200)

    file_path = tmp_path / "stats.png"
    result_path = await service.site_stats_graphic(site.telegram_id_author, site.id, file_path=str(file_path))

    assert result_path == str(file_path)
    assert file_path.exists()


@pytest.mark.asyncio
async def test_get_all_statistic(logs_repo):
    service = LogsService(logs_repo)
    site = DummySite(5, 111)

    await logs_repo.create_log(site, 200, 100)
    await logs_repo.create_log(site, 500, 200)

    uptime, downtime, total = await service.get_all_statistic(site.telegram_id_author, site.id)

    assert total == 2
    assert uptime == 50.0
    assert downtime == 50.0


@pytest.mark.asyncio
async def test_get_week_ago_statistics(logs_repo):
    service = LogsService(logs_repo)
    site = DummySite(6, 222)

    # Лог старше недели
    old_log = Log(site_id=site.id, author_id=site.telegram_id_author, status_code=200, response_time_ms=100,
                  timestamp=datetime.utcnow() - timedelta(days=10))
    # Лог за последнюю неделю
    new_log = Log(site_id=site.id, author_id=site.telegram_id_author, status_code=500, response_time_ms=200,
                  timestamp=datetime.utcnow() - timedelta(days=1))

    logs_repo.session.add_all([old_log, new_log])
    await logs_repo.session.commit()

    uptime, downtime, total = await service.get_week_ago_statistics(site.id, site.telegram_id_author)

    assert total == 1
    assert uptime == 0.0
    assert downtime == 100.0
