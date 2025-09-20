import pytest
from app.db.models import User, Site
from app.db.repositories.UserReposirory import UserRepository


@pytest.mark.asyncio
async def test_create_user(session):
    repo = UserRepository(session)
    user = await repo.create_user(user_id=12345)

    assert user.telegram_id == 12345
    assert user is not None

@pytest.mark.asyncio
async def test_get_user_with_sites(session):
    repo = UserRepository(session)
    user = await repo.create_user(user_id=54321)

    # Добавляем сайты для пользователя
    site1 = Site(telegram_id_author=user.telegram_id, url="https://a.com", check_interval=10)
    site2 = Site(telegram_id_author=user.telegram_id, url="https://b.com", check_interval=20)
    session.add_all([site1, site2])
    await session.commit()

    fetched_user = await repo.get_user_with_sites(user.telegram_id)
    assert fetched_user is not None
    assert len(fetched_user.sites) == 2
    urls = [s.url for s in fetched_user.sites]
    assert "https://a.com" in urls
    assert "https://b.com" in urls
