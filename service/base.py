from typing import Protocol, List
from urllib.parse import urljoin

from loguru import logger

class Response(Protocol):
    content: bytes
    text: str
    
    def raise_for_status(self) -> None: ...

class HasRequest(Protocol):
    def request(*args, **kwargs) -> Response:
        pass
    
    
    
class URL(Protocol): ...

class BaseHttpManager:
    def __init__(
        self,
        session: HasRequest
    ):
        if not hasattr(session, 'request'):
            logger.warning(f"Неподдерживаемый тип: {type(session).__name__}")
            raise TypeError(f"Неподдерживаемый тип: {type(session).__name__}")
        
        self._session = session
    
    def _sync_get(self, url: str | URL, headers: dict[str, str] = {'referer': 'https://anihidecq.org/'}) -> str:
        response = self._session.request(method = "GET", url = url, headers = headers)
        response.raise_for_status()
        
        return response.text
    
    
    
    async def _async_get(self, url: str | URL, headers: dict[str, str] = {'referer': 'https://anihidecq.org/'}) -> str:
        is_httpx = hasattr(self._session, '__class__') and 'httpx' in str(self._session.__class__)
        try:
            if is_httpx:
                raise TypeError()
            async with self._session.request(method="GET", url=url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
            
        except (AttributeError, TypeError):
            response = await self._session.request(method="GET", url=url, headers=headers)
            response.raise_for_status()
            return response.text
        
    async def _async_get_content(self, url: str | URL, headers: dict[str, str] = {'referer': 'https://anihidecq.org/'}) -> bytes:
        is_httpx = hasattr(self._session, '__class__') and 'httpx' in str(self._session.__class__)
        try:
            if is_httpx:
                raise TypeError()
            async with self._session.request(method="GET", url=url, headers=headers) as response:
                response.raise_for_status()
                return await response.read()
            
        except (AttributeError, TypeError):
            response = await self._session.request(method="GET", url=url, headers=headers)
            response.raise_for_status()
            return response.content
        
    def _parse_m3u8_content(self, base_url: str | URL, content: str) -> List[str]:
        result = []
        
        for line in content.splitlines():
            line = line.strip()
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
                
            if any(line.endswith(ext) for ext in ('.m3u8', '.ts', '.m4s', '.mp4')):
                absolute_url = urljoin(base_url, line)
                result.append(absolute_url)
                
        return result