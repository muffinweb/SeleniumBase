# This requires .env file on where this file locates

import httpx
import random
import os
import asyncio
from dotenv import load_dotenv

# Read ENV variable from .env
load_dotenv()

# Secret token provided by ENV
secret_token = os.getenv("secret")

async def list_proxies():
    url = 'https://proxy.webshare.io/api/v2/proxy/list/'
    headers = {
        'Authorization': 'Token ' + secret_token,
    }
    params = {
        'mode': 'direct',
        'page': '1',
        'page_size': '100'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()

async def get_proxy(locale = ""):
    data = await list_proxies()
    proxies = data.get("results")

    if not proxies:
        raise Exception("No proxies found")
    else:
        if(locale == ""):
            chosen_proxy = random.choice(proxies)
            return chosen_proxy
        else:
            found_proxy = next((item for item in proxies if item.get("country_code") == locale.upper()), None)
            return found_proxy

def buildProxyStr(proxyAuth):
    return proxyAuth['username'] + ':' + proxyAuth['password'] + '@' + proxyAuth['proxy_address'] + ':' + str(proxyAuth['port'])


# # Sample usage code is below
# asyncio.run(get_proxies())

#proxyAuth = asyncio.run(get_proxy())
#proxy = buildProxyStr(proxyAuth)
#print(proxy)