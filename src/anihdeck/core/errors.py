class ParseError(Exception):
    """Ощибка при парсинге"""
    
class IncorrectData(Exception):
    """Указывает на то что ожидаемые данные некорректные"""
    
class HTTPError(Exception):
    """Ошибка связаное с HTTP"""