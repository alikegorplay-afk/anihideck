from abc import abstractmethod
from typing import List

from ..base import BaseHttpManager

class BaseM3U8Manager(BaseHttpManager):
    
    @abstractmethod
    def get_m3u8(self, url: str) -> str: ...
    
    @abstractmethod
    def get_m3u8_urls(self, url: str) -> List[str]: ...