import asyncio
from datetime import datetime

import aiohttp
import requests
from bs4 import BeautifulSoup

start = datetime.now()

r = requests.get('https://learn.microsoft.com/en-us/compliance/regulatory/offering-home')
soup = BeautifulSoup(r.text, features='html.parser')

find_a = soup.find_all('a', attrs="has-external-link-indicator")


async def fetch(client, url, index, value):
    async with client.get(url, allow_redirects=False) as resp:
        # assert resp.status == 200
        result = await resp.text()
        if ('Power Platform' in result) or ('Power Automate' in result):
            print(f"{index}: {value.text}")


async def main():
    async with aiohttp.ClientSession() as client:
        tasks = []
        for i, value in enumerate(find_a):
            href = value.get('href')
            if 'https://' not in href:
                real_href = 'https://learn.microsoft.com/en-us/compliance/regulatory/' + href
                tasks.append(asyncio.create_task(fetch(client, real_href, i, value)))
            else:
                tasks.append(asyncio.create_task(fetch(client, href, i, value)))

        await asyncio.wait(tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

end = datetime.now()
print(f'total time spent: {end - start}')
