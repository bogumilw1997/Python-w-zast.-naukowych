# poetry run python .\program9.py
# cd .\lab\lab\lab09\

import json
import aiohttp
import aiofiles
import asyncio
import os

with open('data/links.txt', 'r') as f:
    links = json.load(f)

async def write_img(session, link):
    
    async with session.get(link) as response:
    
        img_name = link.split('/')[-1]
        
        async with aiofiles.open(f'data/{img_name}', mode='wb') as f:
            await f.write(await response.read())
            await f.close()
                
                
async def main(links_list):
    
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        for link in links_list:
            tasks.append(write_img(session, link))
            
        await asyncio.gather(*tasks)
    
asyncio.run(main(links))

