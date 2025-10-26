import asyncio

#from httpx import Client, AsyncClient
from requests import session
#from aiohttp import ClientSession

from src.anihdeck import AniHideck, AsyncAniHideck

BASE_URL = "https://anihidecq.org"
URL = 'https://anihidecq.org/1371-uchi-no-otouto-maji-de-dekain-dakedo-mi-ni-konai.html'

#api = AniHideck(BASE_URL, Client())
#result = api.get_info(URL)
#print(result.id)

api = AniHideck(BASE_URL, session())
result = api.get_info(URL)
print(result.id)

#async def main():
#    async with AsyncClient() as session:
#        api = AsyncAniHideck(BASE_URL, session)
#        result = await api.get_info(URL)
#        print(result.id)
#        
#    async with ClientSession() as session:
#        api = AsyncAniHideck(BASE_URL, session)
#        result = await api.get_info(URL)
#        print(result.id)
#        
#if __name__ == "__main__":
#    asyncio.run(main())