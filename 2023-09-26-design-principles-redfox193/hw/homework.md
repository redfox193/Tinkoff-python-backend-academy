Дано описание требуемой системы:

Необходимо разработать модуль отвечающий за управление участниками курса.
Модуль предоставляет следущие функции:

1. Создавать и редактировать преподавателей
2. Создавать и редактировать слушателей
3. Назначать слушателя на преподавателя
4. Получить список имен слушателей для конкретного преподавателя по его имени,
   если преподаватель не найде бросить исключние

Модуль должен выбрасывать исключение если была попытка назначить несуществующего студента,
либо на несуществующего преподавателя.

Домашнее задание:

1. Сделать ревью кода модуля в [реализации](./before.py), написав в комментариях какие принципы нарушаются
2. Завести Файл `after.py`, в котором внесены исправления в соответствии с проведенным ревью
   (и если потребуется поправить код [тестов](../tests/test_courses_management.py))
3. Проверить что все тесты для модуля отрабатывают корректно
4. Сделать такое же ревью своего кода из прошлого дз, положив исходный код в папку `hw/before` и отписав в комментариях
   найденые
   нарушения принципов. В папке `hw/after` положить переработанный код в соответствии с .