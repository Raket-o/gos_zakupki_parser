"""Модуль очереди задач с celery."""

from typing import Any

import requests
import re
import xmltodict

from bs4 import BeautifulSoup
from celery import Celery, Task
from urllib.parse import urlparse


app = Celery("tasks", broker="redis://192.168.55.4:6379/0", backend="redis://192.168.55.4:6379/0")

URL_PARSER: str = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber="
URL_PARENT: str = f"https://{urlparse(URL_PARSER).netloc}"
HEADERS: dict = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
}


class GetTenderUrlsTask(Task):
    """Задача сбора ссылок с каждой страницы."""
    def run(self, number_page: int = 1) -> set[str]:
        """
        Функция в параметрах получает номер страницы и отправляет GET запрос,
        далее парсит html страницу, вытаскивает url тендеров и возвращат
        их во множестве.
        :param number_page: Номер страницы с которой нужно вытащить url тендера.
        :return: Возвращает множество с url тендеров.
        """
        set_auctions_xml = []
        response = requests.get(url=f"{URL_PARSER}{number_page}", headers=HEADERS, timeout=5)
        bs = BeautifulSoup(response.text, 'lxml')
        items = bs.find_all(class_="w-space-nowrap ml-auto registry-entry__header-top__icon")

        for item in items:
            urls = item.find_all("a", {"target": "_blank"})

            for url in urls:
                set_auctions_xml.append(f"{URL_PARENT}{url.get('href')}")

        return set_auctions_xml


class GetTenderDatetimePublishedTask(Task):
    """Задача парсинга данных из XML-форм."""
    # def run(self, set_urls: set[str]) -> set[str]:
    def run(self, set_urls):
        """
        Функция в параметрах получает множество с url тендеров и
        отправляет GET запрос, далее парсит xml форму, вытаскивает
        дату публикации тендеров и возвращает их во множестве.
        :param set_urls: Множество с url тендеров.
        :return: Возвращает множество с (url - время создания тендера).
        """
        pattern = r'view\.html'
        replacement = 'viewXml.html'
        set_datetime_published = []
        for url in set_urls:
            url_to_xml = re.sub(pattern, replacement, url)
            response = requests.get(url_to_xml, headers=HEADERS, timeout=5)

            for value in xmltodict.parse(response.text).values():
                datetime_published = value.get("commonInfo").get("publishDTInEIS")
                if datetime_published:
                    set_datetime_published.append(f"{url} - {datetime_published}")
                else:
                    set_datetime_published.append(None)

        return set_datetime_published


tender_urls_task = app.register_task(GetTenderUrlsTask)
datetime_published_task = app.register_task(GetTenderDatetimePublishedTask)
