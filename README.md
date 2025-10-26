## Anihdeck

Парсер для работы с сайтом [animehidecq](https://animehidecq.org). Предоставляет минимальный необходимый функционал для работы с сайтом (`get_info`, `download_hentai`). В будущем планируется интеграция с Telegram Bot.

## Преимущества:
- **Универсальность** - поддержка асинхронной и синхронной версий
- **Поддерживаемость** - чистый и структурированный код
- **Гибкость** - поддержка aiohttp, httpx, requests

## Быстрый старт:
1. **Устоновить репозиторй:**
```cmd
pip install git+https://github.com/alikegorplay-afk/anihideck.git
```

2. **Устоновить необходимости:**
```cmd
pip install requirements.txt
```

3. **Использовать:**
```python
from anihdeck import AniHideck
from requests import Session

BASE_URL = "https://animehidecq.org"
URL = 'https://animehidecq.org/1371-uchi-no-otouto-maji-de-dekain-dakedo-mi-ni-konai.html'

api = AniHideck(BASE_URL, Session())
result = api.get_info(URL)