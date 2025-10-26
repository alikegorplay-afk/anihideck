from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import SQLGenres, SQLHentaiMetadata, convert

class BaseDBManager(ABC):
    def __init__(
        self,
        url: str
    ):
        self._engine = create_engine(url)
        self.session_maker: sessionmaker = sessionmaker(url)
    
    @abstractmethod
    def get_hentai(self, id: int) -> Optional[SQLHentaiMetadata]: ...
    
    @abstractmethod
    def find_hentai(self, query: str) -> List[SQLHentaiMetadata]: ...
    
    @abstractmethod
    def filter_by_genres(self, genres: List[str]) -> List[SQLHentaiMetadata]: ...
    
    @abstractmethod
    def filter_by_director(self, director: str) -> List[SQLHentaiMetadata]: ...
    
    @abstractmethod
    def filter_by_studio(self, director: str) -> List[SQLHentaiMetadata]: ...
    
    @abstractmethod
    def filter_by_censorship(self, director: str) -> List[SQLHentaiMetadata]: ...
    
    @abstractmethod
    def filter_by_shikimory(self, minimal: float, maximal: float) -> List[SQLHentaiMetadata]: ...