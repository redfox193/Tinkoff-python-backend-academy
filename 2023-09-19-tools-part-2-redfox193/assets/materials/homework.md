[Вернуться][main]

0. Установить IDE, если вдруг до сих пор обходились без такого инструмента

1. Дописать "Виселицу", или написать новое приложение. Приложение с новым функционалом должно уметь отправлять запрос в
   любой [публичный API][public-api-lists], получать ответ и выводить результат в консоль. 
   Можно использовать только следующие методы: `GET`, `POST`, `PUT`.
   Для отправки запросов в API можно использовать библиотеку [requests][requests], [httpx][httpx] или аналоги.

2. Создать и собрать проект, загрузить на [TestPyPi][pypi], приложить ссылку, проверить корректность установки с помощью
   менеджера пакетов `pip` или `poetry`

3. Упаковать своё приложение в Docker с версией python `3.12.0rc2`

[Ссылка][hw] на ДЗ в Github Classroom.

[Вернуться][main]

---

[main]: ../../README.md "содержание"

[requests]: https://requests.readthedocs.io "HTTP for Humans"

[httpx]: https://www.python-httpx.org "A next-generation HTTP client for Python."

[pypi]: https://test.pypi.org/account/register/ "PyPi"

[public-api-lists]: https://github.com/public-api-lists/public-api-lists "список публичных API"

[hw]: https://classroom.github.com/a/RXF8Hi8J "ДЗ."
