import time
import ssl, certifi
from urllib.parse import urlparse

import aiohttp

class SiteChecker:
    def __init__(self):
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())


    async def check_site(self, url: str):
        """Получает и собирает информацию о сайте"""
        return await self._get_response(url)


    def _normalize_url(self,url: str) -> str:
        """Добавляет https:// если схема не указана"""
        parsed = urlparse(url)
        if not parsed.scheme:
            return "https://" + url
        return url


    async def _get_response(self, url):
        """Отправляет запрос на указанный url"""
        try:
            url = self._normalize_url(url)
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                response = await session.get(url, ssl=self.ssl_context)
                response_time = time.time() - start_time
                content = await response.text()
                status_code = response.status
                return status_code, response_time, content
        except Exception as e:
            return None, None, str(e)