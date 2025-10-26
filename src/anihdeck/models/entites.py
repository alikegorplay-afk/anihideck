from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class HentaiMetadata:
    title: str
    url: str
    poster: Optional[str]
    director: Optional[str]
    premiere: Optional[str]
    studio: Optional[str]
    status: Optional[str]
    subtitles: Optional[List[str]]
    voiceover: Optional[List[str]]
    genres: Optional[List[str]]
    censorship: Optional[str]
    quality: Optional[str]
    description: Optional[str]
    
    shikimori: Optional[str] = None
    
    all_txt: Dict[str, str] = field(default_factory=dict)
    
    @property
    def id(self):
        return int(self.url.split('/')[-1].split('-')[0])
    
@dataclass
class TxtData:
    title: str
    default_quality: str
    poster: str
    file: List[str] = field(default_factory=list)