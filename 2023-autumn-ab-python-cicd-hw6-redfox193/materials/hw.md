На основе предыдещуго дз необходимо:

1. Добавить Dockerfile и docker-compose.yml для тестового и продакшн контейнера
2. Все инструменты должны иметь возможность запускаться через docker контейнер
3. Настроить CI/CD следующий образом:
   ```
   style checks +-> tests ------------- + -> docker build
                \                      /
                  -> security checks -
   ```
   Тесты должны прогоняться внутри контейнера

Дополнительные материалы:

* https://realpython.com/docker-continuous-integration/
* https://docs.github.com/actions
* https://docs.github.com/en/actions/quickstart

Критерии оценки:

| Критерий                                               |   |
|--------------------------------------------------------|---|
| style check использует black flake8 pylint mypy        | 2 |
| test запускает юнит-тесты сервиса в тестовом контенере | 2 |
| security checks использует bandit                      | 2 |
| docker build собирается прод контейнер                 | 2 |
| все шаги успешно отрабатывают                          | 2 |
