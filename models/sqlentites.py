import json

from typing import Optional, List, Dict

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from dataclasses import dataclass

class Base(DeclarativeBase):
    ...

@dataclass
class SQLGenres(Base):
    __tablename__ = "genres"
    
    title: Mapped[str] = mapped_column(String(255), primary_key=True)
    hentai_id: Mapped[int] = mapped_column(
        ForeignKey('hentai.id'),
        primary_key=True
    )
    hentai: Mapped["SQLHentaiMetadata"] = relationship("SQLHentaiMetadata", back_populates="_genres")
    
@dataclass
class SQLHentaiMetadata(Base):
    __tablename__ = "hentai"
    
    id: Mapped[int] = mapped_column(Integer(), primary_key = True)
    
    title: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(255))
    
    poster: Mapped[Optional[str]] = mapped_column(String(255), nullable = True)
    director: Mapped[Optional[str]] = mapped_column(String(255), nullable = True)
    premiere: Mapped[Optional[str]] = mapped_column(String(255), nullable = True)
    studio: Mapped[Optional[str]] = mapped_column(String(255), nullable = True)
    status: Mapped[Optional[str]] = mapped_column(String(255), nullable = True)
    
    subtitles: Mapped[Optional[str]] = mapped_column(String(1024), nullable = True)
    voiceover: Mapped[Optional[str]] = mapped_column(String(1024), nullable = True)
    censorship: Mapped[Optional[str]] = mapped_column(String(255), nullable = True)
    quality: Mapped[Optional[str]] = mapped_column(String(255), nullable = True)
    
    description: Mapped[Optional[str]] = mapped_column(String(2048), nullable = True)
    all_txt: Mapped[Optional[str]] = mapped_column(String(1024), nullable = True)
    shikimori: Mapped[Optional[str]] = mapped_column(String(255), nullable = True)
    
    _genres: Mapped[List["SQLGenres"]] = relationship(
        "SQLGenres", 
        back_populates="hentai",
        cascade="all, delete-orphan"
    )

    @property
    def subtitle(self) -> List[str]:
        return json.loads(self.subtitles) if self.subtitles else []
    
    @subtitle.setter
    def subtitle(self, subtitles: List[str]) -> None:
        self.subtitles = json.dumps(subtitles)
    
    @property
    def txt(self) -> Dict[str, str]:
        return json.loads(self.all_txt) if self.all_txt else {}

    @txt.setter
    def txt(self, txt: Dict[str, str]) -> None:
        self.all_txt = json.dumps(txt)
        
    
    @property
    def voice(self) -> List[str]:
        return json.loads(self.voiceover) if self.voiceover else []
    
    @voice.setter
    def voice(self, voiceover: List[str]) -> None:
        self.voiceover = json.dumps(voiceover)
    
    @property
    def genres(self) -> List[str]:
        return [genre.title for genre in self._genres]
    
    @genres.setter
    def genres(self, genre_titles: List[str]) -> None:
        self._genres = [SQLGenres(title=title, hentai_id=self.id) for title in genre_titles]