from urllib.parse import urlparse
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json


# URL_parser = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
URL_PARSER = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber="
URL_PARENT = f"https://{urlparse(URL_PARSER).netloc}"
QTY_PAGES = 2
HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
    }

"https://zakupki.gov.ru//epz/order/notice/printForm/viewXml.html?regNumber=0361200014125000026"


async def get_auction_links() -> set[str]:
    pattern = r'view\.html'
    replacement = 'viewXml.html'
    set_auctions_xml = set()
    # for num_page in range(1, QTY_PAGES + 1):
    for num_page in range(1, 2):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{URL_PARSER}{num_page}", headers=HEADERS, timeout=5) as response:
                if response.status == 200:
                    bs = BeautifulSoup(await response.text(), 'lxml')
                    # items = bs.find_all(class_="registry-entry__header-mid__number")
                    items = bs.find_all(class_="w-space-nowrap ml-auto registry-entry__header-top__icon")
                    for item in items:
                        urls = item.find_all("a", {"target": "_blank"})
                        for url in urls:
                            result = re.sub(pattern, replacement, url.get("href"))
                            set_auctions_xml.add(f"{URL_PARENT}/{result}")
            await asyncio.sleep(1)

    return set_auctions_xml


async def main():
    set_auction_links = await get_auction_links()
    # print(len(list_auction))
    print(set_auction_links)

    if set_auction_links:
        pass


if __name__ == "__main__":
    asyncio.run(main())
