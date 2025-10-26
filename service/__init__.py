__all__ = [
    "AniHideck",
    "AsyncAniHideck"
]

from pathlib import Path
from typing import LiteralString

from core.hentparser.hentparser import HentaiParser
from core.dataparser.base import M3U8Parser
from models.entites import HentaiMetadata
from .m3u8_manager.manager import M3U8Manager
from .m3u8_manager.manager import AsyncM3U8Manager
from .hentai_manager.manager import HentaiManagerFactory
from .base import HasRequest


class AniHideck:
    """
    Синхронный клиент для работы с хентай-контентом с сайта AniHideck.
    
    Предоставляет методы для получения информации о хентае и его загрузки.
    
    Attributes:
        _session (HasRequest): HTTP-сессия для выполнения запросов
        _base_url (str): Базовый URL целевого сайта
        _manager: Менеджер для управления операциями с хентай-контентом
    """
    
    def __init__(
        self,
        base_url: str,
        session: HasRequest,
        /,
        parse_engine: str = 'html.parser'
    ):
        """
        Инициализирует синхронный клиент AniHideck.
        
        Args:
            base_url (str): Базовый URL сайта для парсинга
            session (HasRequest): Объект сессии с поддержкой HTTP-запросов
            parse_engine (str, optional): Движок для парсинга HTML. 
                                        По умолчанию 'html.parser'
        """
        self._session = session
        self._base_url = base_url
        
        self._manager = HentaiManagerFactory.create_sync_manager(
            session = self._session,
            parser = HentaiParser(self._base_url, parse_engine),
            m3u8_manager = M3U8Manager(self._session),
            m3u8_parser = M3U8Parser()
        )
        
    def get_info(self, url: str) -> HentaiMetadata:
        """
        Получает метаданные о хентае по указанному URL.
        
        Args:
            url (str): URL страницы с хентаем
            
        Returns:
            HentaiMetadata: Объект с метаданными хентая (название, эпизоды, 
                          информация о качестве и т.д.)
        """
        return self._manager.get_hentai(url = url)
        
    def download_hentai(
        self, 
        path_to_save: str | Path,
        txt_url: str,
        quality: LiteralString = "default",
        max_workers: int = 5
    ) -> None:
        """
        Загружает хентай по указанному URL в заданное качество.
        
        Args:
            path_to_save (str | Path): Путь для сохранения загруженного контента
            txt_url (str): URL текстового файла или страницы с ссылками на видео
            quality (LiteralString, optional): Желаемое качество видео. 
                                             По умолчанию "default"
            max_workers (int, optional): Максимальное количество потоков для 
                                       параллельной загрузки. По умолчанию 5
        """
        self._manager.download_hentai(
            path_to_save = path_to_save,
            txt_url = txt_url,
            quality = quality,
            max_workers = max_workers
        )
        
class AsyncAniHideck:
    """
    Асинхронный клиент для работы с хентай-контентом с сайта AniHideck.
    
    Предоставляет асинхронные методы для получения информации о хентае 
    и его загрузки.
    
    Attributes:
        _session (HasRequest): HTTP-сессия для выполнения асинхронных запросов
        _base_url (str): Базовый URL целевого сайта
        _manager: Асинхронный менеджер для управления операциями с хентай-контентом
    """
    
    def __init__(
        self,
        base_url: str,
        session: HasRequest,
        /,
        parse_engine: str = 'html.parser'
    ):
        """
        Инициализирует асинхронный клиент AniHideck.
        
        Args:
            base_url (str): Базовый URL сайта для парсинга
            session (HasRequest): Объект сессии с поддержкой асинхронных HTTP-запросов
            parse_engine (str, optional): Движок для парсинга HTML. 
                                        По умолчанию 'html.parser'
        """
        self._session = session
        self._base_url = base_url
        
        self._manager = HentaiManagerFactory.create_async_manager(
            session = self._session,
            parser = HentaiParser(self._base_url, parse_engine),
            m3u8_manager = AsyncM3U8Manager(self._session),
            m3u8_parser = M3U8Parser()
        )
        
    async def get_info(self, url: str) -> HentaiMetadata:
        """
        Асинхронно получает метаданные о хентае по указанному URL.
        
        Args:
            url (str): URL страницы с хентаем
            
        Returns:
            HentaiMetadata: Объект с метаданными хентая (название, эпизоды, 
                          информация о качестве и т.д.)
        """
        return await self._manager.get_hentai(url = url)
        
    async def download_hentai(
        self, 
        path_to_save: str | Path,
        txt_url: str,
        quality: LiteralString = "default",
        max_workers: int = 5
    ) -> None:
        """
        Асинхронно загружает хентай по указанному URL в заданное качество.
        
        Args:
            path_to_save (str | Path): Путь для сохранения загруженного контента
            txt_url (str): URL текстового файла или страницы с ссылками на видео
            quality (LiteralString, optional): Желаемое качество видео. 
                                             По умолчанию "default"
            max_workers (int, optional): Максимальное количество потоков для 
                                       параллельной загрузки. По умолчанию 5
        """
        await self._manager.download_hentai(
            path_to_save = path_to_save,
            txt_url = txt_url,
            quality = quality,
            max_workers = max_workers
        )