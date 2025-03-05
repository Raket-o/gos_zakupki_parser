import asyncio

from tasks import datetime_published_task, tender_urls_task

QTY_PAGES = 2


def main():
    for num_page in range(1, QTY_PAGES + 1):
        tender_urls_list = tender_urls_task.run(num_page)
        datetime_published_task(tender_urls_list)


if __name__ == "__main__":
    main()
