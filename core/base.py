from urllib.parse import urljoin

from bs4 import Tag
from loguru import logger


class BaseParser:
    def __init__(
        self,
        base_url: str,
        engine: str = 'html.parser'
    ):
        self._base_url = base_url
        self._engine = engine
        
    def _safe_extract_url(self, tag: Tag, attr: str) -> str:
        if not tag or not attr:
            logger.warning("Отсутствует один из важных атрибутов")
            return ""
        
        if url := tag.get(attr):
            logger.debug(f"Успешно был получен URL: {url}")
            return urljoin(self._base_url, url)
        
        logger.warning(f"URL не найден")
        return ""