"""Модуль запуска."""

import asyncio

from celery import chain

from tasks import datetime_published_task, tender_urls_task

QTY_PAGES: int = 2  # Количество страниц для парсинга


def main() -> None:
    """
    Главная функция запуска.
    """
    for num_page in range(1, QTY_PAGES + 1):
        task1 = tender_urls_task.s(number_page=num_page)
        task2 = datetime_published_task.s()
        task_chain = chain(task1 | task2)
        result = task_chain.apply_async()
        print(*result.get(), sep="\n")


if __name__ == "__main__":
    main()
