import re
import sys

from functools import lru_cache
from collections import defaultdict
from typing import Dict

from bs4 import BeautifulSoup
from loguru import logger
from loguru._defaults import LOGURU_FORMAT

from .base import BaseHentaiParser
from ..errors import ParseError

logger.remove()
logger.add(
    sys.stdout,
    format = LOGURU_FORMAT.replace(".SSS", ""),
    level="INFO"
)


class HentaiParser(BaseHentaiParser):
    
    def _extract_title(self, soup):
        """Извлекает заголовок хентая из HTML-структуры."""
        logger.debug("Начало извлечения заголовка")
        if title := self._find_text(soup, ".page__header h1"):
            logger.info(f"Успешно извлечен заголовок: {title}")
            return title
        
        logger.error("Не удалось извлечь обязательный атрибут 'title'")
        raise ParseError("Не найден обязательный атрибут 'title'")
    
    def _extract_url(self, soup):
        """Извлекает канонический URL страницы."""
        logger.debug("Начало извлечения URL")
        if url := self._safe_extract_url(
            soup.select_one('link[rel="canonical"]'),
            'href'
        ):
            logger.info(f"Успешно извлечен URL: {url}")
            return url
        
        logger.error("Не удалось извлечь обязательный атрибут 'URL'")
        raise ParseError("Не найден обязательный атрибут 'URL'")
    
    def _extract_poster(self, soup):
        """Извлекает URL постера хентая."""
        logger.debug("Начало извлечения постера")
        poster_url = self._safe_extract_url(soup.select_one('.pmovie__poster.img-fit-cover img'), "data-src")
        if poster_url:
            logger.info(f"Успешно извлечен URL постера: {poster_url}")
        else:
            logger.warning("Постер не найден на странице")
        return poster_url
    
    def _extract_director(self, soup):
        """Извлекает информацию о режиссере."""
        logger.debug("Начало извлечения данных о режиссере")
        director_data = self._extract_all_data(soup).get('Режиссер')
        result = ''.join(director_data) if director_data else None
        logger.debug(f"Данные о режиссере: {result}")
        return result
    
    def _extract_premiere(self, soup):
        """Извлекает дату премьеры."""
        logger.debug("Начало извлечения даты премьеры")
        premiere_data = self._extract_all_data(soup).get('Премьера')
        result = ''.join(premiere_data) if premiere_data else None
        logger.debug(f"Дата премьеры: {result}")
        return result
    
    def _extract_studio(self, soup):
        """Извлекает информацию о студии."""
        logger.debug("Начало извлечения данных о студии")
        studio_data = self._extract_all_data(soup).get('Студия')
        result = ''.join(studio_data) if studio_data else None
        logger.debug(f"Данные о студии: {result}")
        return result
    
    def _extract_status(self, soup):
        """Извлекает статус хентая."""
        logger.debug("Начало извлечения статуса")
        status_data = self._extract_all_data(soup).get('Статус')
        result = ''.join(status_data) if status_data else None
        logger.debug(f"Статус хентая: {result}")
        return result
    
    def _extract_subtitles(self, soup):
        """Извлекает информацию о субтитрах."""
        logger.debug("Начало извлечения данных о субтитрах")
        subtitles = self._extract_all_data(soup).get('Субтитры')
        logger.debug(f"Данные о субтитрах: {subtitles}")
        return subtitles

    def _extract_voiceover(self, soup):
        """Извлекает информацию об озвучке."""
        logger.debug("Начало извлечения данных об озвучке")
        voiceover = self._extract_all_data(soup).get('Озвучка')
        logger.debug(f"Данные об озвучке: {voiceover}")
        return voiceover

    def _extract_genres(self, soup):
        """Извлекает список жанров."""
        logger.debug("Начало извлечения жанров")
        genres_data = self._extract_all_data(soup).get('Жанр', [])
        genres_data = ''.join(genres_data)
        
        if ',' in genres_data:
            genres_list = [tag.strip() for tag in (genres_data).split(',')] if genres_data else []
        else:
            genres_list = (genres_data).split(' / ') if genres_data else []
            
        logger.info(f"Извлечено жанров: {len(genres_list)} - {genres_list}")
        return genres_list

    def _extract_quality(self, soup):
        """Извлекает информацию о качестве."""
        logger.debug("Начало извлечения данных о качестве")
        quality_data = self._extract_all_data(soup).get('Качество')
        result = ''.join(quality_data) if quality_data else None
        logger.debug(f"Качество видео: {result}")
        return result
    
    def _extract_censorship(self, soup):
        """Извлекает информацию о цензуре."""
        logger.debug("Начало извлечения данных о цензуре")
        censorship_data = self._extract_all_data(soup).get('Цензура')
        result = ''.join(censorship_data) if censorship_data else None
        logger.debug(f"Данные о цензуре: {result}")
        return result
    
    def _extract_description(self, soup):
        """Извлекает описание хентая."""
        logger.debug("Начало извлечения описания")
        description = self._find_text(soup, ".page__text.full-text.clearfix")
        if description:
            desc_preview = description[:100] + "..." if len(description) > 100 else description
            logger.info(f"Извлечено описание: {desc_preview}")
        else:
            logger.warning("Описание не найдено")
        return description
    
    def _extract_shikimori_id(self, soup):
        """Извлекает Shikimori."""
        logger.debug("Начало извлечения Shikimori")
        shikimori_id = self._find_text(soup, 'div[data-text="Shikimori"]')
        if shikimori_id:
            logger.info(f"Извлечен Shikimori: {shikimori_id}")
        else:
            logger.debug("Shikimori не найден")
        return shikimori_id
    
    def _extract_txt_data(self, soup):
        """Извлекает дополнительные данные из скриптов."""
        logger.debug("Начало извлечения дополнительных данных из скриптов")
        data = {}
        scripts_found = 0
        
        for script in self._find_all_text(soup, 'div .reclama script'):
            match = re.search(self.TXT_PATTERN, script)
            if match:
                data[match.group(1)] = match.group(2)
                scripts_found += 1
                logger.debug(f"Извлечен скрипт с ключом: {match.group(1)}")
        
        logger.info(f"Извлечено дополнительных данных из скриптов: {scripts_found}")
        return data
    
    @lru_cache(1)   
    def _extract_all_data(self, soup: BeautifulSoup) -> Dict[str, list[str]]:
        """Извлекает все основные данные из информационного блока страницы."""
        logger.debug("Начало извлечения всех основных данных из страницы")
        data = defaultdict(list)
        unexpected_data_count = 0
        
        info_block = soup.select_one('div.page__subcols.d-flex')
        if not info_block:
            logger.warning("Информационный блок 'div.page__subcols.d-flex' не найден")
            return data
            
        elements = info_block.select('li')
        logger.debug(f"Найдено информационных элементов: {len(elements)}")
        
        for i, element in enumerate(elements):
            txt = element.get_text(strip=True).split(':')
            if len(txt) == 2:
                key, value = txt
                data[key].append(value)
                logger.debug(f"Обработан элемент: {key} = {value}")
            else:
                unexpected_data_count += 1
                logger.warning(f"Неожиданные данные в элементе {i}: {txt}")
        
        if unexpected_data_count > 0:
            logger.warning(f"Всего неожиданных данных: {unexpected_data_count}")
            
        logger.info(f"Успешно извлечено {len(data)} категорий данных")
        return data