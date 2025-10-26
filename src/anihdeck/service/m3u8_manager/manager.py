from typing import List, Optional

from .base import BaseM3U8Manager

class M3U8Manager(BaseM3U8Manager):
    
    def get_m3u8(self, url: str) -> str:
        return self._sync_get(url)
    
    def get_m3u8_urls(self, url: str) -> List[str]:
        content = self._sync_get(url)
        return self._parse_m3u8_content(url, content)
    
    def get_by_quality(self, urls: List[str], quality: str = '480p') -> Optional[List[str]]:
        for url in urls:
            if quality in url:
                return self.get_m3u8_urls(url)
        return None

class AsyncM3U8Manager(BaseM3U8Manager):
    
    async def get_m3u8(self, url: str) -> str:
        return await self._async_get(url)
    
    async def get_m3u8_urls(self, url: str) -> List[str]:
        content = await self._async_get(url)
        return self._parse_m3u8_content(url, content)
    
    async def get_by_quality(self, urls: List[str], quality: str = '480p') -> Optional[List[str]]:
        for url in urls:
            if quality in url:
                return await self.get_m3u8_urls(url)
        return None
