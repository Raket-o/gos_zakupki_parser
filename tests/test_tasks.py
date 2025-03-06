"""Модуль тестов"""

import unittest

from tasks import GetTenderUrlsTask, GetTenderDatetimePublishedTask


class TestTasks(unittest.TestCase):
    def test_tender_urls_task(self) -> None:
        """
        Тест задачи GetTenderUrlsTask. Запускает функцию run у класса GetTenderUrlsTask.
        Проверяет, приходят ли данные (с URL_PARSER из модуля tasks.py)
        Сравнивает каждый url с начальным.
        """
        task = GetTenderUrlsTask()
        set_tender_urls = task.run()
        self.assertNotEqual(len(set_tender_urls), 0)

        for ulr in set_tender_urls:
            self.assertEqual(ulr[:49], "https://zakupki.gov.ru/epz/order/notice/printForm")

    def test_tender_datetime_published_task(self) -> None:
        """
        Тест задачи GetTenderDatetimePublishedTask.
        Запускает функцию run класса GetTenderDatetimePublishedTask
        и передаёт множество tender_urls.
        Проверяет tender_datetime_urls с результатом запроса.
        """
        tender_urls = {
            "https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0320100018025000003",
            "https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0320100018025000004"
        }

        tender_datetime_urls = {
                'https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0320100018025000004 - 2025-02-28T11:13:07.908+10:00',
                'https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0320100018025000003 - 2025-02-28T11:16:09.544+10:00'
            }
        task = GetTenderDatetimePublishedTask()
        set_datetime_published = task.run(tender_urls)
        self.assertEqual(set_datetime_published, tender_datetime_urls)
