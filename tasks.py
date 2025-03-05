# from collections import OrderedDict
# from typing import Any
#
# import aiohttp
# import asyncio
#
# import re
# import xmltodict
#
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
#
# from celery import Celery, Task
#
# from bs4 import BeautifulSoup
#
#
# app = Celery("tasks", broker="redis://192.168.55.4:6379/0", backend="redis://192.168.55.4:6379/0")
#
# URL_PARSER = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber="
# URL_PARENT = f"https://{urlparse(URL_PARSER).netloc}"
# HEADERS = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
# }
#
#
# class TenderUrlsTask(Task):
#     async def run(self, number_page=1) -> set[str]:
#         pattern = r'view\.html'
#         replacement = 'viewXml.html'
#         set_auctions_xml = set()
#         url = f"{URL_PARSER}{number_page}"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=HEADERS, timeout=5) as response:
#                 if response.status == 200:
#                     bs = BeautifulSoup(await response.text(), 'lxml')
#                     items = bs.find_all(class_="w-space-nowrap ml-auto registry-entry__header-top__icon")
#                     for item in items:
#                         urls = item.find_all("a", {"target": "_blank"})
#                         for url in urls:
#                             result = re.sub(pattern, replacement, url.get("href"))
#                             set_auctions_xml.add(f"{URL_PARENT}{result}")
#                     await asyncio.sleep(0.5)
#                 else:
#                     print(f"{url} = status {response.status}")
#         return set_auctions_xml
#
#
# class TenderDetailsTask(Task):
#     async def run(self, list_urls: list[str]) -> None:
#         for url in list_urls:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url, headers=HEADERS, timeout=5) as response:
#                     if response.status == 200:
#                         for value in xmltodict.parse(await response.text()).values():
#                             datetime_published = value.get("commonInfo").get("publishDTInEIS")
#                             print(f"{url} - {datetime_published}")
#                         await asyncio.sleep(0.5)
#                     else:
#                         print(f"{url} = status {response.status}")
#
#
# tender_urls_task = app.register_task(TenderUrlsTask)
# datetime_published_task = app.register_task(TenderDetailsTask)


from collections import OrderedDict
from typing import Any

import aiohttp
import asyncio
import requests

import re
import xmltodict

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from celery import Celery, Task

from bs4 import BeautifulSoup


app = Celery("tasks", broker="redis://192.168.55.4:6379/0", backend="redis://192.168.55.4:6379/0")

URL_PARSER = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber="
URL_PARENT = f"https://{urlparse(URL_PARSER).netloc}"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
}


class TenderUrlsTask(Task):
    def run(self, number_page=1) -> set[str]:
        pattern = r'view\.html'
        replacement = 'viewXml.html'
        set_auctions_xml = set()
        url = f"{URL_PARSER}{number_page}"
        response = requests.get(url, headers=HEADERS, timeout=5)
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url, headers=HEADERS, timeout=5) as response:
        #         # if response.status == 200:
        bs = BeautifulSoup(response.text, 'lxml')
        items = bs.find_all(class_="w-space-nowrap ml-auto registry-entry__header-top__icon")
        for item in items:
            urls = item.find_all("a", {"target": "_blank"})
            for url in urls:
                result = re.sub(pattern, replacement, url.get("href"))
                set_auctions_xml.add(f"{URL_PARENT}{result}")
                    # await asyncio.sleep(0.5)
                # else:
                #     print(f"{url} = status {response.status}")
        return set_auctions_xml


class TenderDetailsTask(Task):
    def run(self, list_urls: list[str]) -> None:
        for url in list_urls:
            response = requests.get(url, headers=HEADERS, timeout=5)

            # async with aiohttp.ClientSession() as session:
            #     async with session.get(url, headers=HEADERS, timeout=5) as response:
            #         if response.status == 200:
            for value in xmltodict.parse(response.text).values():
                datetime_published = value.get("commonInfo").get("publishDTInEIS")
                print(f"{url} - {datetime_published}")
                        # await asyncio.sleep(0.5)
                    # else:
                    #     print(f"{url} = status {response.status}")


tender_urls_task = app.register_task(TenderUrlsTask)
datetime_published_task = app.register_task(TenderDetailsTask)


