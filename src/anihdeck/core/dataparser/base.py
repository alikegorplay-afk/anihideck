import json

from typing import List, Dict, Iterable, IO

from ..errors import IncorrectData
from ...models.entites import TxtData

class M3U8Parser:
    def loads(self, s: str | bytes | bytearray | IO[str] | IO[bytes]) -> List[TxtData]:
        if hasattr(s, 'read'):
            s = s.read()
            
        result: List[TxtData] = []
        
        try:
            data: List[Dict[str, str]] = json.loads(s)
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Невалидный Json")
        
        if not isinstance(data, Iterable):
            logger.error("Нерверный обьект, ожидалось что обьект итерируемый")
            raise IncorrectData("Неитерируемый обьект")
        
        for seria in data:
            result.append(
                TxtData(
                    title = seria.get('title'),
                    poster = seria.get('poster'),
                    default_quality = seria.get('default_quality'),
                    file = self._parse_file(seria.get('file'))
                )
            )
            
        return result
    
    def _parse_file(self, data: str) -> List[str]:
        if not data:
            raise IncorrectData("Ожидаемый объект отстутствует")
        
        return data.split(' and ')