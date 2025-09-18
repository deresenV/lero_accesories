from aiogram import Router

from .StartRouter import StartRouter
from .UserWebsitesRouter import UserWebsitesRouter
from .AddWebsiteRouter import AddWebSiteRouter

routers = Router()

routers.include_router(AddWebSiteRouter().router)
routers.include_router(StartRouter().router)
routers.include_router(UserWebsitesRouter().router)