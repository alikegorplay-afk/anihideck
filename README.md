## Anihdeck

Парсер для работы с сайтом [anihidecq.org](https://anihidecq.org/). Предоставляет минимальный необходимый функционал для работы с сайтом (`get_info`, `download_hentai`). В будущем планируется интеграция с Telegram Bot.

## Преимущества:
- **Универсальность** — поддержка асинхронной и синхронной версий.
- **Поддерживаемость** — чистый и структурированный код.
- **Гибкость** — поддержка aiohttp, httpx, requests, urlib3 и тп.

## Быстрый старт:
1. **Установить репозиторий:**
```cmd
pip install git+https://github.com/alikegorplay-afk/anihideck.git
```

2. **Установить необходимости:**
```cmd
pip install requirements.txt
```

3.**Установить любой HTTP клент**
```cmd
pip install requests # Но можно и httpx, aiohttp, urlib3...
```

4. **Использовать:**
```python
from anihdeck import AniHideck
from requests import Session

BASE_URL = "https://animehidecq.org"
URL = 'https://animehidecq.org/1371-uchi-no-otouto-maji-de-dekain-dakedo-mi-ni-konai.html'

api = AniHideck(BASE_URL, Session())
result = api.get_info(URL)
```
