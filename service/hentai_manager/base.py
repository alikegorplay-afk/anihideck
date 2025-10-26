from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, Union

from ..base import BaseHttpManager
from models.entites import HentaiMetadata



class BaseHentaiManager(BaseHttpManager, ABC):
    """Абстрактный базовый класс для менеджеров хентая."""
    
    @abstractmethod
    async def get_hentai(self, url: str) -> HentaiMetadata:
        """Получить информацию о хентае по URL."""
        pass
    
    @abstractmethod
    async def get_quality_urls(self, txt_url: str, quality: str = 'default') -> List[Tuple[str, List[str]]]:
        """Получить URL видео указанного качества."""
        pass
    
    @abstractmethod
    async def download_hentai(
        self, 
        path_to_save: Union[str, Path], 
        txt_url: str, 
        quality: str = "default",
        max_workers: int = 5
    ) -> None:
        """Скачать хентай."""
        pass