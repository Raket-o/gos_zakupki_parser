"""Модуль запуска."""

import asyncio

from tasks import datetime_published_task, tender_urls_task

QTY_PAGES: int = 2  # Количество страниц для парсинга


def main() -> None:
    """
    Главная функция запуска.
    """
    for num_page in range(1, QTY_PAGES + 1):
        tender_urls_list = tender_urls_task.run(num_page)
        result = datetime_published_task(tender_urls_list)
        print(*result, sep="\n")


if __name__ == "__main__":
    main()
