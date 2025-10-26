import asyncio
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tempfile import TemporaryDirectory
from pathlib import Path
from hashlib import sha256
from typing import List, Tuple, Any, Union

import aiofiles
from loguru import logger

from ..base import HasRequest
from ...models.entites import HentaiMetadata
from ...core.hentparser.hentparser import BaseHentaiParser
from ...core.dataparser.base import M3U8Parser
from ..m3u8_manager.manager import BaseM3U8Manager
from .base import BaseHentaiManager

class SyncHentaiManager(BaseHentaiManager):
    """Синхронная реализация менеджера хентая."""
    
    def __init__(
        self, 
        session: Any,
        parser: BaseHentaiParser,
        m3u8_manager: BaseM3U8Manager,
        m3u8_parser: M3U8Parser
    ):
        """
        Инициализировать синхронный менеджер хентая.
        
        Args:
            session: HTTP сессия
            parser: Парсер хентая
            m3u8_manager: Менеджер M3U8
            m3u8_parser: Парсер M3U8
        """
        super().__init__(session)
        self._parser = parser
        self._m3u8_manager = m3u8_manager
        self._m3u8_parser = m3u8_parser
    
    def get_hentai(self, url: str) -> Any:
        """
        Получить информацию о хентае по URL.
        
        Args:
            url: URL хентая
            
        Returns:
            Распарсенная информация о хентае
        """
        response = self._sync_get(url)
        return self._parser.parse_hentai(response)
    
    def get_quality_urls(self, txt_url: str, quality: str = 'default') -> List[Tuple[str, List[str]]]:
        """
        Получить URL видео указанного качества.
        
        Args:
            txt_url: URL текстового файла с M3U8 плейлистом
            quality: Желаемое качество видео
            
        Returns:
            Список кортежей (название, список URL сегментов)
        """
        urls: List[Tuple[str, List[str]]] = []
        
        try:
            response = self._m3u8_manager.get_m3u8(txt_url)
            m3u8_entries = self._m3u8_parser.loads(response)
        except Exception as e:
            logger.error(f"Ошибка загрузки M3U8 плейлиста {txt_url}: {e}")
            return urls
        
        for m3u8_entry in m3u8_entries:
            current_quality = quality
            if current_quality == 'default':
                current_quality = m3u8_entry.default_quality
            
            found_urls = False
            for file_url in m3u8_entry.file:
                try:
                    m3u8_urls = self._m3u8_manager.get_m3u8_urls(file_url)
                    
                    matching_urls = [
                        url for url in m3u8_urls 
                        if current_quality in url
                    ]
                    
                    if matching_urls:
                        urls.append((m3u8_entry.title, self._m3u8_manager.get_m3u8_urls(matching_urls[0])))
                        found_urls = True
                        break
                        
                except Exception as e:
                    logger.error(f"Ошибка обработки URL {file_url}: {e}")
                    continue
            
            if not found_urls:
                logger.warning(
                    f"Не найдено URL с качеством '{current_quality}' "
                    f"для '{m3u8_entry.title}'"
                )
        
        return urls
    
    def _download_chunk(self, url: str, path: Path) -> None:
        """
        Скачать чанк видео.
        
        Args:
            url: URL чанка
            path: Путь для сохранения
        """
        logger.info(f"Скачивание чанка: {path.name}")
        with open(path, 'wb') as f:
            f.write(self._sync_get_content(url))
            
        logger.success(f"Успешно скачан чанк: {path.name}")
    
    def _concat_videos(self, txts: List[Tuple[str, Path]], output_dir: Path, ffmpeg: str | Path) -> None:
        """
        Объединить видео чанки в финальные файлы.
        
        Args:
            txts: Список кортежей (название, путь к файлу со списком чанков)
            output_dir: Директория для сохранения результатов
            ffmpeg: Путь/Команда для работы с ffpmeg
        """
        futures = []
        with ThreadPoolExecutor() as executor:
            for title, txt in txts:
                output_path = output_dir / f"{title}.mp4"
                futures.append(executor.submit(
                    subprocess.run,
                    [
                        ffmpeg,
                        "-f", "concat",
                        "-safe", "0",
                        "-i", str(txt),
                        "-c", "copy",
                        "-y",
                        str(output_path)
                    ]
                ))
            
            for future in futures:
                future.result()
    
    def download_hentai(
        self, 
        path_to_save: Union[str, Path], 
        txt_url: str, 
        quality: str = "default",
        max_workers: int = 5,
        /,
        ffmpeg: str | Path = "ffmpeg"
    ) -> None:
        """
        Скачать хентай.
        
        Args:
            path_to_save: Путь для сохранения
            txt_url: URL текстового файла с M3U8 плейлистом
            quality: Качество видео
            max_workers: Максимальное количество потоков
            ffmpeg: Путь/Команда для работы с ffpmeg
        """
        path_to_save = Path(path_to_save) / "Temp"
        urls = self.get_quality_urls(txt_url, quality)
        
        path_to_save.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=path_to_save) as tmpdir:
            txts = []
            futures = []
            tmpdir = Path(tmpdir)
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Скачивание чанков
                for title, segment_urls in urls:
                    txt = tmpdir / f"{title}.txt"
                    txts.append((title, txt))
                    
                    with open(txt, 'w') as file:
                        for url in segment_urls:
                            ts_filename = sha256(url.encode()).hexdigest() + Path(url).name
                            ts_path = tmpdir / ts_filename
                            futures.append(
                                executor.submit(self._download_chunk, url, ts_path)
                            )
                            file.write(f"file '{ts_path.absolute()}'\n")
                
                # Ожидание завершения загрузки чанков
                for future in futures:
                    future.result()
                
                # Объединение чанков в видео
                self._concat_videos(txts, path_to_save.parent, ffmpeg)

class AsyncHentaiManager(BaseHentaiManager):
    """Асинхронная реализация менеджера хентая."""
    
    def __init__(
        self, 
        session: HasRequest,
        parser: BaseHentaiParser,
        m3u8_manager: BaseM3U8Manager,
        m3u8_parser: M3U8Parser
    ):
        """
        Инициализировать асинхронный менеджер хентая.
        
        Args:
            session: Асинхронная HTTP сессия
            parser: Парсер хентая
            m3u8_manager: Менеджер M3U8
            m3u8_parser: Парсер M3U8
        """
        self._session = session
        self._parser = parser
        self._m3u8_manager = m3u8_manager
        self._m3u8_parser = m3u8_parser
    
    async def get_hentai(self, url: str) -> HentaiMetadata:
        """
        Получить информацию о хентае по URL.
        
        Args:
            url: URL хентая
            
        Returns:
            Распарсенная информация о хентае
        """
        
        content = await self._async_get(url)
        return self._parser.parse_hentai(content)
    
    async def get_quality_urls(self, txt_url: str, quality: str = 'default') -> List[Tuple[str, List[str]]]:
        """
        Получить URL видео указанного качества.
        
        Args:
            txt_url: URL текстового файла с M3U8 плейлистом
            quality: Желаемое качество видео
            
        Returns:
            Список кортежей (название, список URL сегментов)
        """
        urls: List[Tuple[str, List[str]]] = []
        
        try:
            response = await self._m3u8_manager.get_m3u8(txt_url)
            m3u8_entries = self._m3u8_parser.loads(response)
        except Exception as e:
            logger.error(f"Ошибка загрузки M3U8 плейлиста {txt_url}: {e}")
            return urls
        
        for m3u8_entry in m3u8_entries:
            current_quality = quality
            if current_quality == 'default':
                current_quality = m3u8_entry.default_quality
            
            found_urls = False
            for file_url in m3u8_entry.file:
                try:
                    m3u8_urls = await self._m3u8_manager.get_m3u8_urls(file_url)
                    
                    matching_urls = [
                        url for url in m3u8_urls 
                        if current_quality in url
                    ]
                    
                    if matching_urls:
                        segment_urls = await self._m3u8_manager.get_m3u8_urls(matching_urls[0])
                        urls.append((m3u8_entry.title, segment_urls))
                        found_urls = True
                        break
                        
                except Exception as e:
                    logger.error(f"Ошибка обработки URL {file_url}: {e}")
                    continue
            
            if not found_urls:
                logger.warning(
                    f"Не найдено URL с качеством '{current_quality}' "
                    f"для '{m3u8_entry.title}'"
                )
        
        return urls
    
    async def _download_chunk(self, url: str, path: Path) -> None:
        """
        Скачать чанк видео асинхронно.
        
        Args:
            url: URL чанка
            path: Путь для сохранения
        """
        logger.info(f"Скачивание чанка: {path.name}")
        
        async with aiofiles.open(path, 'wb') as f:
            await f.write(await self._async_get_content(url))
        logger.success(f"Успешно скачан чанк: {path.name}")
    
    async def _download_chunks(
        self, 
        urls: List[Tuple[str, List[str]]], 
        tmpdir: Path,
        max_workers: int
    ) -> List[Tuple[str, Path]]:
        """
        Скачать все чанки асинхронно.
        
        Args:
            urls: Список кортежей (название, список URL сегментов)
            tmpdir: Временная директория
            max_workers: Максимальное количество одновременных запросов
            
        Returns:
            Список кортежей (название, путь к файлу со списком чанков)
        """
        semaphore = asyncio.Semaphore(max_workers)
        txts = []
        
        async def download_with_semaphore(url: str, path: Path) -> None:
            async with semaphore:
                await self._download_chunk(url, path)
        
        tasks = []
        for title, segment_urls in urls:
            txt = tmpdir / f"{title}.txt"
            txts.append((title, txt))
            
            chunk_tasks = []
            for url in segment_urls:
                ts_filename = sha256(url.encode()).hexdigest() + Path(url).name
                ts_path = tmpdir / ts_filename
                chunk_tasks.append(download_with_semaphore(url, ts_path))
            
            # Создаем файл со списком чанков
            async with aiofiles.open(txt, 'w') as file:
                for url in segment_urls:
                    ts_filename = sha256(url.encode()).hexdigest() + Path(url).name
                    ts_path = tmpdir / ts_filename
                    await file.write(f"file '{ts_path.absolute()}'\n")
            
            tasks.extend(chunk_tasks)
        
        # Параллельное скачивание всех чанков
        await asyncio.gather(*tasks)
        return txts
    
    async def _concat_videos_async(self, txts: List[Tuple[str, Path]], output_dir: Path) -> None:
        """
        Объединить видео чанки в финальные файлы асинхронно.
        
        Args:
            txts: Список кортежей (название, путь к файлу со списком чанков)
            output_dir: Директория для сохранения результатов
        """
        tasks = []
        for title, txt in txts:
            output_path = output_dir / f"{title}.mp4"
            process = await asyncio.create_subprocess_exec(
                "C:/ffmpeg/bin/ffmpeg.exe",
                "-f", "concat",
                "-safe", "0",
                "-i", str(txt),
                "-c", "copy",
                "-y",
                str(output_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            tasks.append(process)
        
        # Ожидаем завершения всех процессов ffmpeg
        for process in tasks:
            await process.wait()
    
    async def download_hentai(
        self, 
        path_to_save: Union[str, Path], 
        txt_url: str, 
        quality: str = "default",
        max_workers: int = 5
    ) -> None:
        """
        Скачать хентай асинхронно.
        
        Args:
            path_to_save: Путь для сохранения
            txt_url: URL текстового файла с M3U8 плейлистом
            quality: Качество видео
            max_workers: Максимальное количество одновременных запросов
        """
        path_to_save = Path(path_to_save) / "Temp"
        urls = await self.get_quality_urls(txt_url, quality)
        
        path_to_save.mkdir(parents=True, exist_ok=True)
        
        with TemporaryDirectory(dir=path_to_save) as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Скачиваем все чанки
            txts = await self._download_chunks(urls, tmpdir, max_workers)
            
            # Объединяем чанки в видео
            await self._concat_videos_async(txts, path_to_save.parent)


# Фабрика для создания менеджеров
class HentaiManagerFactory:
    """Фабрика для создания менеджеров хентая."""
    
    @staticmethod
    def create_sync_manager(
        session: Any,
        parser: BaseHentaiParser,
        m3u8_manager: BaseM3U8Manager,
        m3u8_parser: M3U8Parser
    ) -> SyncHentaiManager:
        """
        Создать синхронный менеджер хентая.
        
        Args:
            session: HTTP сессия
            parser: Парсер хентая
            m3u8_manager: Менеджер M3U8
            m3u8_parser: Парсер M3U8
            
        Returns:
            Синхронный менеджер хентая
        """
        return SyncHentaiManager(session, parser, m3u8_manager, m3u8_parser)
    
    @staticmethod
    def create_async_manager(
        session: HasRequest,
        parser: BaseHentaiParser,
        m3u8_manager: BaseM3U8Manager,
        m3u8_parser: M3U8Parser
    ) -> AsyncHentaiManager:
        """
        Создать асинхронный менеджер хентая.
        
        Args:
            session: Асинхронная HTTP сессия
            parser: Парсер хентая
            m3u8_manager: Менеджер M3U8
            m3u8_parser: Парсер M3U8
            
        Returns:
            Асинхронный менеджер хентая
        """
        return AsyncHentaiManager(session, parser, m3u8_manager, m3u8_parser)