from abc import ABC, abstractmethod
from typing import Any, Optional

from bs4 import BeautifulSoup, _IncomingMarkup

from ..base import BaseParser
from ...models.entites import HentaiMetadata

class BaseHentaiParser(BaseParser, ABC):
    TXT_PATTERN = r'Playerjs\(\{id:"([^"]+)",\s*file:"([^"]+)"\}\)'
    """
    Абстрактный базовый парсер для извлечения метаданных хентая.
    
    Реализует шаблонный метод parse_hentai, оставляя конкретную
    реализацию извлечения данных подклассам.
    """
    
    def parse_hentai(self, data: _IncomingMarkup) -> HentaiMetadata:
        """
        Основной метод парсинга хентая.
        
        Args:
            data: Входные данные для парсинга (HTML, XML, etc.)
            
        Returns:
            HentaiMetadata: Объект с извлеченными метаданными
            
        Raises:
            ParseError: Если не удалось распарсить данные
        """
        soup = BeautifulSoup(data, self._engine)

        return HentaiMetadata(
            title=self._extract_title(soup),
            poster=self._extract_poster(soup),
            url = self._extract_url(soup),
            director=self._extract_director(soup),
            premiere=self._extract_premiere(soup),
            studio=self._extract_studio(soup),
            status=self._extract_status(soup),
            subtitles=self._extract_subtitles(soup),
            voiceover=self._extract_voiceover(soup),
            genres=self._extract_genres(soup),
            censorship=self._extract_censorship(soup),
            quality=self._extract_quality(soup),
            description=self._extract_description(soup),
            shikimori=self._extract_shikimori_id(soup),
            all_txt=self._extract_txt_data(soup)
        )
    
    @abstractmethod
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Извлекает название хентая."""
        pass
    
    @abstractmethod
    def _extract_url(self, soup: BeautifulSoup):
        """Извлекает URL хентая."""
        pass
    
    def _extract_poster(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает постер. Базовая реализация возвращает None."""
        return None
    
    def _extract_director(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает режиссера. Базовая реализация возвращает None."""
        return None
    
    def _extract_premiere(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает дату премьеры. Базовая реализация возвращает None."""
        return None
    
    def _extract_studio(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает студию. Базовая реализация возвращает None."""
        return None
    
    def _extract_status(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает статус. Базовая реализация возвращает None."""
        return None
    
    def _extract_subtitles(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает информацию о субтитрах. Базовая реализация возвращает None."""
        return None
    
    def _extract_voiceover(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает информацию о озвучке. Базовая реализация возвращает None."""
        return None
    
    def _extract_genres(self, soup: BeautifulSoup) -> Optional[list[str]]:
        """Извлекает список жанров. Базовая реализация возвращает None."""
        return None
    
    def _extract_censorship(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает информацию о цензуре. Базовая реализация возвращает None."""
        return None
    
    def _extract_quality(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает информацию о качестве. Базовая реализация возвращает None."""
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает описание. Базовая реализация возвращает None."""
        return None
    
    def _extract_shikimori_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает ID Shikimori. Базовая реализация возвращает None."""
        return None
    
    def _extract_txt_data(self, soup: BeautifulSoup) -> Optional[str]:
        """Извлекает текстовые данные. Базовая реализация возвращает None."""
        return None
    
    # Вспомогательные методы для подклассов
    def _find_text(self, soup: BeautifulSoup, selector: str, default: Any = None) -> Any:
        """Вспомогательный метод для извлечения текста по CSS селектору."""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else default
    
    def _find_attr(self, soup: BeautifulSoup, selector: str, attr: str, default: Any = None) -> Any:
        """Вспомогательный метод для извлечения атрибута по CSS селектору."""
        element = soup.select_one(selector)
        return element.get(attr) if element else default
    
    def _find_all_text(self, soup: BeautifulSoup, selector: str) -> list[str]:
        """Вспомогательный метод для извлечения всех текстов по CSS селектору."""
        return [el.get_text(strip=True) for el in soup.select(selector)]