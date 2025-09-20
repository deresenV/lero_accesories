import pytest
from app.db.repositories.SiteRepository import SiteRepository
from app.db.models import Site

@pytest.mark.asyncio
async def test_create_site(session):
    repo = SiteRepository(session)
    site = await repo.create_site(user_id="123", url="https://example.com", interval=60)

    assert site.id is not None
    assert site.telegram_id_author == "123"
    assert site.url == "https://example.com"
    assert site.check_interval == 60

@pytest.mark.asyncio
async def test_get_site_by_id(session):
    repo = SiteRepository(session)
    site = await repo.create_site(user_id="456", url="https://get.com", interval=30)

    fetched_site = await repo.get_site_by_id(site.id)
    assert fetched_site.id == site.id
    assert fetched_site.url == "https://get.com"

@pytest.mark.asyncio
async def test_update_site_url(session):
    repo = SiteRepository(session)
    site = await repo.create_site(user_id="789", url="https://old.com", interval=15)

    updated_site = await repo.update_site_url(site.id, "https://new.com")
    assert updated_site.url == "https://new.com"

@pytest.mark.asyncio
async def test_get_all_sites(session):
    repo = SiteRepository(session)
    await repo.create_site(user_id="1", url="https://a.com", interval=10)
    await repo.create_site(user_id="2", url="https://b.com", interval=20)

    sites = await repo.get_all_sites()
    assert len(sites) >= 2
    urls = [s.url for s in sites]
    assert "https://a.com" in urls
    assert "https://b.com" in urls

@pytest.mark.asyncio
async def test_update_site_interval(session):
    repo = SiteRepository(session)
    site = await repo.create_site(user_id="101", url="https://interval.com", interval=5)

    updated_site = await repo.update_site_interval(site.id, 50)
    assert updated_site.check_interval == 50

@pytest.mark.asyncio
async def test_delete_site(session):
    repo = SiteRepository(session)
    site = await repo.create_site(user_id="202", url="https://delete.com", interval=5)

    deleted = await repo.delete_site(site.id)
    assert deleted is True

    # Проверяем, что сайт больше не существует
    fetched_site = await repo.get_site_by_id(site.id)
    assert fetched_site is None

@pytest.mark.asyncio
async def test_delete_nonexistent_site(session):
    repo = SiteRepository(session)
    deleted = await repo.delete_site(9999)  # ID, которого нет
    assert deleted is False
