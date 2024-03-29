[Вернуться][main]

# IDE

## Pycharm

Есть много хороших и разных IDE, например `Vim`, `Notepad++`, `Atom`, `Sublime Text`, `Visual Studio Code` и другие,
но сегодня мы поговорим о PyCharm

- Скачать можно по [ссылке][download]
- Подробный [гайд][install_guide] по установке

После успешной установки и запуска будет примерно такая картина:

![][img_0]

Можно кастомизировать под себя, установить плагины, настроить темы и многое другое.

## Создаём проект

Почему именно "проекты"?

Допустим, вам нужно создать проект. В этом заключается основное отличие IDE, подобной PyCharm, от текстовых редакторов.

PyCharm отлично анализирует весь ваш код в проекте, а затем позволяет вам очень продуктивно перемещаться по нему,
редактировать, проводить массовый рефакторинг, предупреждать о проблемах и многое другое.

Но кодирование - это не только редактирование файлов. У вас также есть рабочие процессы разработки: запуск кода, отладка
кода, консоль Python, системный терминал, тесты, покрытие, профилирование, контроль версий, базы данных, фронтенды... и
т.д. Проект - это центральное представление всего этого для вашего кода в виде последовательного, качественного и
привычного пользовательского интерфейса.

## Интерпретаторы

В проектах на Python лучше всего работать, создавая виртуальную среду. В этом случае каждый проект ведет себя так, как
будто у него есть свой собственный Python. Если вы установите некоторые пакеты в одном проекте, это не приведет к
поломке другого проекта.

PyCharm позаботится об этом, создав и активировав виртуальную среду для вашего нового проекта. Вернемся к экрану "Новый
проект", где есть раздел "Интерпретатор Python: New Virtualenv environment. В нашем случае мы собираемся создать новую
среду с помощью virtualenv, но, как вы видите, PyCharm также поддерживает PipEnv и Conda из коробки.

У нас уже установлен Python 3.11 в качестве Python по умолчанию. PyCharm обнаружил его, поэтому мы можем нажать кнопку
Create.

![][img_01]

## Редактор

Когда файл открыт, он отображается на одной из вкладок редактора. При двойном щелчке на другом файле открывается еще
одна вкладка. Как вы понимаете, их можно закрывать и организовывать по отдельности различными способами.

Внутри редактора, с правой стороны, находится виджет проверки, с помощью которого можно просмотреть все проблемы в
текущем файле и переходить от одной проблемы к другой.

![][img_02]

В полосах прокрутки можно также увидеть ошибки и предупреждения. В левой части редактора в желобе отображаются номера
строк, пиктограммы, а нажатие на желоб позволяет выполнить ряд действий, например, добавить или удалить точки останова.

Щелчком правой кнопки мыши в любом месте панели редактора можно вызвать контекстное меню, в котором отображается список
действий, доступных в текущем контексте. Для некоторых действий появляются всплывающие окна, позволяющие перейти к
выполнению действия. В нижней части панели редактора также можно увидеть хлебные крошки. Они показывают имена классов,
переменных, функций, методов и тегов в текущем открытом файле. С их помощью можно быстро перемещаться по исходному коду.

## Окна инструментов

IDE стремится помочь вам в написании кода и интегрировать другие процессы разработки. Для этого в ней предусмотрены окна
инструментов, которые служат для выполнения определенных задач. По умолчанию слева открыто окно Project (⌘1 + | Alt+1),
в котором отображается схема расположения файлов проекта.

Окно Терминал позволяет работать со встроенным терминалом. Окно инструментов Python Packages позволяет управлять
пакетами из Pypi и других репозиториев в контексте виртуальной среды.

Окно инструментов Python Console представляет собой интерактивную консоль Python, позволяющую выполнять команды и
скрипты Python построчно в контексте интерпретатора проекта. Она удобна для исследования.

![][img_03]

В самом низу IDE находится строка состояния. Это небольшая, но очень удобная часть пользовательского интерфейса.
Во-первых, это кнопка быстрого доступа. Она позволяет быстро переключаться между окнами инструментов, а также скрывать и
показывать панель окон инструментов. В правой части строки состояния расположено несколько полезных виджетов строки
состояния, включая настройки проекта, информацию о контроле версий и настройку интерпретатора проекта.

В верхней части также находится панель навигации. Она служит быстрой альтернативой окну инструмента Project для
перемещения по каталогам и выполнения операций с файлами.

Кроме того, с помощью кнопок, расположенных справа от панели навигации, можно быстро выполнить некоторые общие действия,
например, запустить или отладить приложение, обновить проект или сделать фиксацию, запустить поиск и т.п. Обратите
внимание, что панель инструментов может выглядеть иначе, если ваш проект не находится под контролем версий.

Эта часть пользовательского интерфейса также открывает доступ к Code With Me - встроенной в PyCharm функциональности для
совместной разработки. Здесь можно разрешить доступ гостям и начать сеанс совместной работы.

Наконец, прямо над панелью навигации находится главное меню. Оно содержит различные действия и элементы управления, в
том числе Параметры/Настройки и Справка.

## Клонирование проекта

Второе место, где можно настроить интерпретатор, - это клонирование проекта из VCS. На экране PyCharm Getting Started
можно нажать кнопку Get from VCS.

Мы можем вставить URL-адрес репозитория, принять сгенерированный выбор каталога для клонирования и нажать кнопку Clone.

![][img_04]

PyCharm открывает новый проект в этом каталоге и начинает клонировать репозиторий. После завершения клонирования PyCharm
создает интерпретатор проекта, основанный на Python по умолчанию, и начинает установку пакетов, указанных в файле
требований.

## Пресеты для запуска скриптов

![][img_05]

## Docker и многое другое ...

[Вернуться][main]

---

[main]: ../../README.md "содержание"

[download]: https://www.jetbrains.com/pycharm/download/?section=mac "Скачать PyCharm"

[install_guide]: https://www.jetbrains.com/help/pycharm/installation-guide.html#standalone "Установить PyCharm"

[img_0]: ../img/ide/img.png

[img_01]: ../img/ide/img_1.png

[img_02]: ../img/ide/img_2.png

[img_03]: ../img/ide/img_3.png

[img_04]: ../img/ide/img_4.png

[img_05]: ../img/ide/img_5.png
