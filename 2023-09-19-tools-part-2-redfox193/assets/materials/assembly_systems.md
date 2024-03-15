[Вернуться][main]

# Системы сборки

## Суть

**Системы сборки** - это наборы утилит, функций и инструкций, которые автоматизируют процесс компиляции исходного
кода и его преобразования в исполняемые программы или библиотеки.

**Цель системы сборки Python** - минимизация ручного труда, обеспечение переносимости и максимальной автоматизации
стадий разработки, включая тестирование, сборку, развертывание и распространение программ.

## Обзор систем сборки: [setuptools][setuptools], [distutils][distutils]

**setuptools** - популярный инструмент для создания и распространения пакетов Python. Он предлагает возможности,
такие как установка из исходных текстов, автоматическая компиляция расширений C и многое другое.

**distutils** - это стандартный инструмент сборки Python, входящий в стандартную библиотеку Python. Он обеспечивает
базовые функции для сборки и распространения пакетов Python, включая упаковку, распаковку, создание исполняемых файлов и
т.д.

## Создание и сборка проекта с помощью setuptools

Описываем метаданные проекта, это можно сделать как в файле [pyproject.toml][pyproject],
так и в отдельном: setup.cfg или setup.py

Предположим, что у нас есть следующая структура проекта:

```
/python-hw-2-template
/src
  /homework_docker
    __init__.py
  setup.py
  README.md
```

где `python-hw-2-template` - это корневой каталог проекта, `homework_docker` - это пакет Python, который мы создаем,
setup.py - это скрипт настройки `setuptools`, а `README.md` - это файл с описанием проекта.

Содержимое файла setup.py может выглядеть следующим образом:

```python
from setuptools import setup, find_packages

setup(
    name="hw-2",
    version="0.1",
    packages=find_packages(),
)
```

Для запуска процесса сборки, мы запустим следующую команду в командной строке:

```bash
python -m build
```

Эта команда создаст дистрибутив исходного кода и дистрибутив binary wheel в директории `dist` вашего проекта.

[Документация][docs]

[TestPyPi][pypi]

[Вернуться][main]

---

[main]: ../../README.md "содержание"

[pyproject]: ../../pyproject.toml "pyproject.toml"

[setuptools]: https://setuptools.pypa.io/en/latest/ "setuptools"

[distutils]: https://docs.python.org/3/library/distutils.html "distutils"

[docs]: https://packaging.python.org/en/latest/tutorials/packaging-projects/ "Документация" 

[pypi]: https://test.pypi.org/account/register/ "PyPi" 
