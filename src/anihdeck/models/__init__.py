__all__ = [
    "HentaiMetadata",
    "TxtData",
    "Base",
    "convert"
]

import json

from typing import List, Tuple, Union, overload

from .entites import HentaiMetadata, TxtData
#from .sqlentites import SQLGenres, SQLHentaiMetadata, Base

#HENTAI = Union[HentaiMetadata, SQLHentaiMetadata]
#RESULT = Union[
#    Tuple[SQLHentaiMetadata, List[SQLGenres]],
#    HentaiMetadata
#]
#
#@overload
#def convert(hentai: HentaiMetadata) -> Tuple[SQLHentaiMetadata, List[SQLGenres]]: ...
#
#@overload
#def convert(hentai: SQLHentaiMetadata, tags: List[SQLGenres]) -> HentaiMetadata: ...
#
#def convert(hentai: HENTAI, *args) -> RESULT:
#    if isinstance(hentai, HentaiMetadata):
#        # Преобразование из HentaiMetadata в SQLHentaiMetadata и List[SQLGenres]
#        sql_hentai = SQLHentaiMetadata(
#            id=hentai.id,
#            title=hentai.title,
#            url=hentai.url,
#            poster=hentai.poster,
#            director=hentai.director,
#            premiere=hentai.premiere,
#            studio=hentai.studio,
#            status=hentai.status,
#            subtitles = json.dumps(hentai.subtitles) if hentai.subtitles else None,
#            voiceover = json.dumps(hentai.voiceover) if hentai.voiceover else None,
#            censorship=hentai.censorship,
#            quality=hentai.quality,
#            description=hentai.description,
#            all_txt = json.dumps(hentai.all_txt) if hentai.all_txt else None,
#            shikimori = hentai.shikimori
#        )
#
#        genres = []
#        if hentai.genres:
#            genres = [SQLGenres(title=genre, hentai_id=hentai.id) for genre in hentai.genres]
#        
#        return (sql_hentai, genres)
#    
#    elif isinstance(hentai, SQLHentaiMetadata):
#        # Преобразование из SQLHentaiMetadata и List[SQLGenres] в HentaiMetadata
#        tags = args[0] if args else []
#        
#        # Используем свойство voice для десериализации JSON
#        voiceover_list = hentai.voice
#        
#        # Используем свойство txt для десериализации JSON
#        all_txt_dict = hentai.txt
#        
#        return HentaiMetadata(
#            title=hentai.title,
#            url=hentai.url,
#            poster=hentai.poster,
#            director=hentai.director,
#            premiere=hentai.premiere,
#            studio=hentai.studio,
#            status=hentai.status,
#            subtitles=hentai.subtitles,
#            voiceover=voiceover_list,
#            genres=[tag.title for tag in tags],
#            censorship=hentai.censorship,
#            quality=hentai.quality,
#            description=hentai.description,
#            shikimori=hentai.shikimori,
#            all_txt=all_txt_dict
#        )