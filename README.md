<div style="text-align: center;">
<img src="images_readme/logo.png" width="550"/>
<h1>Парсер сайта государственных закупок (ЕИС)</h1>
</div>
Программа парсит данные сс страниц раздела "Поиск тендеров" 
на сайте Единой информационной системы в сфере закупок (ЕИС)

Парсинг осуществляется для тендеров, относящихся к 44-ФЗ. 
Для каждой записи собирается ссылка на её печатную форму, 
а также дата публикации (поле `publishDTInEIS`) из 
соответствующего XML-документа.

---
## Запуск программы
### <img src="images_readme/docker.svg" width="40" alt="docker"/> Запуск черех docker.
Запуск через Docker-compose:
Открываем терминал, переходим в корневую папку с проектом:

1. Создаём образ командой ```docker-compose build```
2. Поднимаем контейнер ```docker-compose up```


---
### Выходные данные
Результат выводится в консоли в формате:
```
Ссылка на форму тендера — Дата публикации
```

Пример вывода:
```
https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=0338300047925000011 - 2025-02-27T12:21:53.164+12:00
https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=0547600000825000001 - 2025-03-07T00:04:48.674+11:00
https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=0322200030725000009 - 2025-03-01T18:51:00.597+10:00
https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=0322200001225000218 - 2025-03-03T17:40:00.631+10:00
https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=0322200001225000203 - 2025-03-03T17:42:31.901+10:00
https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=0322200001225000204 - 2025-03-03T17:41:54.258+10:00
```
Если поле `publishDTInEIS` отсутствует в XML-файле, будет выведено `None`.

---
### <img src="images_readme/tests.jpg" width="50"/> Тестирование.
Приложение покрыто unit-тестами и проверено линтерами (black, isort, flake8, mypy).

<img src="images_readme/cover_tests.png" width="450"/>

---
<h2>Лицензия</h2>
Проект распространяется под лицензией MIT.
