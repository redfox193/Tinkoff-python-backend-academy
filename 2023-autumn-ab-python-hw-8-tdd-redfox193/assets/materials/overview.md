[Вернуться][main]

# О чём?

Изобретенная более полувека назад, хэш-таблица является классической структурой данных, которая имеет фундаментальное
значение для программирования. И по сей день она помогает решать многие реальные задачи, например, индексировать таблицы
баз данных, кэшировать вычисляемые значения или реализовывать множества. Она часто встречается на собеседованиях при
приеме на работу, а в языке Python хэш-таблицы используются повсеместно, делая поиск по имени практически мгновенным.

Несмотря на то, что Python поставляется с собственной хэш-таблицей dict, может быть полезно понять, как работают
хэш-таблицы под капотом. В задачах по написанию код вам могут дать задачу создать такую таблицу. На семинаре мы
рассмотрим пошагово реализацию хэш-таблицы с нуля, как если бы в Python её не было. По пути вы столкнетесь с
несколькими задачами, которые введут в курс дела важные понятия и дадут вам представление о том, почему хэш-таблицы так
быстры.

Кроме того, вы получите практику по экстремальной разработке (TDD), которую мы будем применять при создания хэш-таблицы.

На семинаре узнаем:

- Чем хэш-таблица отличается от словаря
- Как реализовать хэш-таблицу с нуля в Python
- Как бороться с хэш-коллизиями и другими проблемами
- Каковы желаемые свойства хэш-функции
- Как работает функция `hash()` в Python под капотом.

# Знакомство со структурой данных хэш-таблицы

Прежде чем углубиться в эту тему, необходимо ознакомиться с терминологией, поскольку она может быть несколько
запутанной. В разговорной речи термин "хэш-таблица" (hash table) или "хэш-карта" (hash map) часто используется
как взаимозаменяемый со словом "словарь" (dictionary). Однако между этими понятиями есть тонкая разница,
поскольку первый термин более специфичен, чем второй.

## Хэш-таблица vs словарь

В информатике словарь - это абстрактный тип данных, состоящий из ключей и значений, расположенных попарно. Кроме того,
он определяет следующие операции над этими элементами:

- Добавить пару ключ-значение
- Удалить пару ключ-значение
- Обновить пару ключ-значение
- Найти значение, связанное с заданным ключом.

В некотором смысле этот абстрактный тип данных напоминает двуязычный словарь, где ключами являются иностранные слова, а
значениями - их определения или переводы на другие языки. Однако не всегда между ключами и значениями должно быть
ощущение эквивалентности. Другим примером словаря является телефонный справочник, в котором имена и фамилии объединены с
соответствующими номерами телефонов.

> **Примечание:**
>
> Всякий раз, когда вы сопоставляете одну вещь с другой или связываете значение с ключом, вы, по сути,
> используете некий словарь. Поэтому словари также называют картами (maps) или ассоциативными массивами.

Словари обладают несколькими интересными свойствами. Одно из них заключается в том, что словарь можно рассматривать как
математическую функцию, которая проецирует один или несколько аргументов ровно на одно значение. Из этого факта вытекают
следующие прямые следствия:

- **Только пары ключ-значение**: В словаре не может быть ключа без значения или наоборот. Они всегда идут вместе.
- **Произвольные ключи и значения**: Ключи и значения могут принадлежать двум непересекающимся множествам одного и того
  же или разных типов. И ключи, и значения могут быть практически любыми, например, числами, словами или даже
  картинками.
- **Неупорядоченные пары ключ-значение**: В связи с предыдущим пунктом словари обычно не определяют порядок пар
  ключ-значение. Однако это может быть специфично для конкретной реализации.
- **Уникальные ключи**: Словарь не может содержать дублирующихся ключей, поскольку это нарушает определение функции.
- **Неуникальные значения**: Одно и то же значение может быть связано со многими ключами, но не обязательно.

Существуют родственные понятия, расширяющие представление о словаре. Например, мультикарта ([multimap][multimap])
позволяет иметь более одного значения на ключ, а двунаправленная карта не только сопоставляет ключи со значениями, но и
обеспечивает сопоставление в обратном направлении. Однако на текущем семинаре мы будем рассматривать только обычный
словарь, в котором каждому ключу соответствует ровно одно значение.

Приведем графическое изображение гипотетического словаря, в котором некоторые абстрактные понятия сопоставляются с
соответствующими им английскими словами:

![][img]

Это односторонняя карта ключей и значений, которые представляют собой два совершенно разных набора элементов. Сразу же
можно заметить, что значений меньше, чем ключей, поскольку слово bow является омонимом с несколькими значениями. Однако
концептуально этот словарь все равно содержит четыре пары. В зависимости от того, как его реализовать, можно повторно
использовать повторяющиеся значения для экономии памяти или дублировать их для простоты.

Итак, как же закодировать такой словарь в языке программирования? Правильный ответ - никак, потому что большинство
современных языков предоставляют словари либо в виде примитивных типов данных, либо в виде классов в стандартных
библиотеках. Python поставляется со встроенным типом `dict`, который уже обернут высокооптимизированной структурой
данных,
написанной на языке C, так что вам не придется писать словарь самостоятельно.

С помощью `dict` в Python можно выполнять все операции со словарями, перечисленные в начале этого раздела:

```python
glossary = {"T-edu": "Backend Academy"}
glossary["exam"] = "Extra Hard Exam"  # Добавить
glossary["T-edu"] = "Seminar TDD 07.11.23"  # Обновить
del glossary["exam"]  # Удалить
print(glossary["T-edu"])  # Найти
## >> 'Seminar TDD 07.11.23'
print(glossary)
## >> {'T-edu': 'Seminar TDD 07.11.23'}
```

С помощью синтаксиса квадратных скобок `[ ]` можно добавить в словарь новую пару ключ-значение. Также можно обновить
значение или удалить существующую пару, обозначенную ключом. Наконец, можно найти значение, связанное с данным ключом.

При этом можно задать и другой вопрос. Как на самом деле работает встроенный словарь? Как он сопоставляет ключи
произвольных типов данных и как он делает это так быстро?

Поиск эффективной реализации этого абстрактного типа данных известен как проблема словаря. Одно из наиболее известных
решений использует структуру данных хэш-таблицы, которую мы сейчас рассмотрим. Однако следует отметить, что это не
единственный способ реализации словаря в общем случае. Другая популярная реализация строится на основе красно-черного
дерева.

## Хэш-таблица: Массив с хэш-функцией

Задумывались ли вы когда-нибудь, почему доступ к элементам последовательности в Python работает так быстро, независимо
от того, какой индекс вы запрашиваете? Допустим, вы работаете с очень длинной строкой символов, как, например, в этом
примере:

```python
import string

text = string.ascii_uppercase * 100_000_000

print(text[:50])
# >> 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWX'

print(len(text))
# >> 2600000000
```

В приведенной выше текстовой переменной 2,6 млрд. символов из повторяющихся ASCII-букв, которые можно подсчитать с
помощью функции `len()`. При этом получить первый, средний, последний или любой другой символ из этой строки
можно одинаково быстро:

```python
print(text[0])  # первый элемент
# >> 'A'

print(text[len(text) // 2])  # средний
# >> 'A'

print(text[-1])  # последний, альтернатива: text[len(text) - 1]
# >> 'Z'
```

То же самое справедливо для всех типов последовательностей в Python, таких как списки и кортежи. Как это происходит?
Секрет такой молниеносной скорости заключается в том, что последовательности в Python опираются на массив, который
представляет собой структуру данных с произвольным доступом. Она основана на двух принципах:

- Массив занимает непрерывный блок памяти.
- Каждый элемент массива имеет фиксированный размер, который известен заранее.

Если известен адрес памяти массива, который называется смещением, то можно мгновенно перейти к нужному элементу массива,
вычислив достаточно простую формулу:

$$ адресЭлемента = смещение + (размерЭлемента * индексЭлемента) $$

Начнём со смещения массива, которое одновременно является адресом первого элемента массива с индексом ноль. Далее вы
продвигаетесь вперед, добавляя необходимое количество байт, которое получается умножением размера элемента на индекс
целевого элемента. Умножение и сложение нескольких чисел всегда занимает одинаковое количество времени.

> Примечание:
>
> В отличие от массивов, списки в Python могут содержать разнородные элементы разного размера, что нарушает приведенную
> выше формулу. Чтобы смягчить эту проблему, Python добавляет еще один уровень непрямой связи, вводя массив указателей
> на места в памяти, а не храня значения непосредственно в массиве:
>
> ![][img_1]
>
> Указатели - это просто целые числа, которые всегда занимают одинаковое количество места. Адреса памяти принято
> обозначать шестнадцатеричной системой счисления. В Python и некоторых других языках такие числа обозначаются с помощью
> префикса `0x`.

Итак, вы знаете, что найти элемент в массиве можно быстро, независимо от того, где этот элемент находится физически.
Можно ли использовать ту же идею в словаре? Да!

Хэш-таблицы получили свое название от трюка, называемого хэшированием (hashing), который позволяет преобразовать
произвольный ключ в целое число, которое может работать как индекс в обычном массиве. Таким образом, вместо того чтобы
искать значение по числовому индексу, вы будете искать его по произвольному ключу без заметного снижения
производительности.

На практике хэширование работает не со всеми ключами, но большинство встроенных типов в Python можно хэшировать. Если вы
будете следовать нескольким правилам, то сможете создавать и свои собственные хэшируемые типы.

[Вернуться][main]

---

[main]: ../../README.md "содержание"

[multimap]: https://en.wikipedia.org/wiki/Multimap "multimap"

[img]: ../img/overview/img.png

[img_1]: ../img/overview/img_1.png