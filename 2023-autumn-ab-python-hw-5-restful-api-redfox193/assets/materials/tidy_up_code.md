[Вернуться][main]

# Приведение кода в порядок

На предыдущем этапе мы соединили API сокращателя URL с базой данных. Написанный нами код работал, но в нем было
несколько
недостатков. Если вы потратите немного времени на то, чтобы привести код в порядок сейчас, то в перспективе реализация
новых функций станет более удобной.

В конце этого шага вы не только получите кодовую базу, на которую можно опираться. Но и более чистый код, который может
даже порадовать.

---

## Выявление недостатков в коде

Рефакторинг кода сопряжен с риском того, что это бесконечное занятие. Как в рисовании, где вы постоянно стираете, чтобы
улучшить линию, вы можете потратить неограниченное время на поиск улучшений в вашей кодовой базе.

Хорошей идеей является ограничение масштабов процесса рефакторинга. Для этого нужно просмотреть свой код и перечислить
недостатки, которые вы хотите устранить.

Не пугайтесь! В целом ваш код жизнеспособен и работает. Однако, как мы обнаружили на предыдущем этапе, функции
`create_url()` и `forward_to_target_url()` в файле `main.py` ещё не идеальны.

Начнем с того, что посмотрим на текущее состояние функции `create_url()`:

```python linenums="1"
# shortener_app/main.py

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url
```

В строке 8 алфавит жестко закодирован как значение символов. Если к строке необходимо добавить еще и цифры, то их ввод
может оказаться громоздким.

Наверняка, вам уже рассказали о принципе Don't Repeat Yourself (**DRY**) для поддержания чистоты кода. Строки 9 и 10
выглядят практически одинаково. То, как вы конструируете переменные `key` и `secret_key`, является прекрасным примером
не DRY-кода.

В строках 11-16 происходит взаимодействие с базой данных. Это действие не должно напрямую касаться `create_url()`. В
`create_url()` вы хотите определить, какие данные ожидает ваша конечная точка и что она должна возвращать. В идеале
вычисление данных следует поручить другим функциям.

В конце функции, в строках 17 и 18, вы взаимодействуете с объектом базы данных для создания ответа `schemas.URLInfo`. Вы
не пытаетесь сохранить эту часть в базе данных, так что вреда от этого нет. Но в приведенных строках должно быть более
очевидное разделение взаимодействия с базой данных.

В общем, функция `create_url()` слишком нагружена различными действиями. Читая код, трудно понять назначение функции.

Далее рассмотрим функцию `forward_to_target_url()`:

```python linenums="1"
# shortener_app/main.py

@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
):
    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
```

В строках с 9 по 13 выполняется действие с базой данных. Как и в `create_url()`, взаимодействие с базой данных в
функции,
определяющей конечную точку API, кажется неправильным.

Далее мы рассмотрим недостатки, найденные в `create_url()` и `forward_to_target_url()`, и устраним их один за другим.


---

## Рефакторинг кода

В этом разделе вы создадите два новых файла для разделения задач вашего приложения. Попутно будут определены функции для
разделения обязанностей. В итоге вы получите более чистый `create_url()`, который будет гораздо лучше читаться.

Начните с создания нового файла с именем `keygen.py`. Этот файл будет содержать все вспомогательные функции для
генерации
ключей для вашего проекта. Это идеальное место для создания случайной строки, необходимой для атрибутов `.url` и
`.admin_url`:

```python linenums="1"
# shortener_app/keygen.py

import secrets
import string


def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))
```

Вместо хардкода букв от A до Z используется модуль `string`, который объединяет все заглавные символы `ASCII` и
цифры в символы. Затем с помощью модуля `secrets` случайным образом выбираются пять символов из `chars` и возвращается
выборка.

Аналогичный результат можно получить и с помощью модуля `random`. Однако при создании случайных строк, используемых в
качестве секретных ключей, рекомендуется использовать модуль `secrets`. В [PEP 506][506] модуль `secrets` был
представлен как
стандартный модуль Python для генерации криптографически защищенных случайных байтов и строк.

Выделив создание случайной строки в отдельную функцию, вы можете удобно протестировать ее в интерпретаторе Python:

```python linenums="1"
from shortener_app.keygen import create_random_key

create_random_key()
create_random_key(length=8)
```

```
'FJAN2'
'QX0Y8BOF'
```

При вызове функции `create_random_key()` без аргументов выдается строка из пяти символов. В вашем случае эта строка,
вероятно, отличается от строки в приведенном примере. Но она должна содержать заглавные буквы, цифры или и то, и другое.

Далее создайте файл `crud.py`. Файл `crud.py` будет содержать функции, выполняющие действия по созданию, чтению,
обновлению и удалению (**Create, Read, Update, and Delete - CRUD**) элементов в вашей базе данных.
Добавьте функцию `create_db_url()`:

```python linenums="1"
# shortener_app/crud.py

from sqlalchemy.orm import Session

from . import keygen, models, schemas


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.create_random_key()
    secret_key = keygen.create_random_key(length=8)
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
```

Прежде чем подробно остановиться на этом коде, обратите внимание на одну проблему в его реализации. Помните, что
значение ключа записи в базе данных должно быть уникальным. Хотя вероятность этого невелика, но возможно, что
`keygen.create_random_key()` вернет уже существующий ключ.

Поэтому необходимо убедиться в том, что нет записи с таким же ключом. Сначала определим функцию, которая сообщает,
существует ли уже ключ в базе данных:

```python linenums="1"
# shortener_app/crud.py

# ...

def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
```

Эта функция возвращает либо `None`, либо запись в базе данных с заданным ключом.

Теперь можно создать функцию, обеспечивающую генерацию уникального ключа. Вернитесь в `keygen.py` и добавьте функцию
`create_unique_random_key()`:

```python linenums="1"
# shortener_app/keygen.py

# ...

from sqlalchemy.orm import Session

from . import crud


# ...

def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
```

Цикл `while` является наиболее важной частью `create_unique_random_key()`. Вы снова вызываете `create_random_key()`,
если ключ уже существует в вашей базе данных. Такая логика позволяет убедиться,
что каждый сокращенный URL существует только один раз.

Добавив эту функцию, обновите функцию `create_db_url()` в файле `crud.py`:

```python linenums="1"
# shortener_app/crud.py

# ...

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
```

В строке 6 выполняется вызов `keygen.create_unique_random_key()` для получения уникальной строки для ключа сокращенного
URL. Вызов `keygen.create_unique_random_key()` гарантирует, что в базе данных не будет двух дубликатов ключей.

Обратите внимание, что вызов `keygen.create_random_key()` выполняется в строке 7 для построения строки secret_key.
Как вы уже узнали, `keygen.create_random_key()` только создает случайную строку, но не проверяет,
существует ли она в базе данных.

Тем не менее, вы можете быть уверены, что `secret_key` уникален, так как вы префиксируете строку значением `key`. Таким
образом, даже если `keygen.create_random_key()` возвращает строку, уже созданную когда-то ранее, то, поместив перед ней
уникальный ключ, вы сделаете уникальной всю строку.

Подобное создание `secret_key` имеет два преимущества:

- Префикс ключа указывает, какому сокращенному URL принадлежит `secret_key`.
- Вы не обращаетесь к базе данных при создании очередной случайной строки.

Вернитесь в `main.py` и обновите `create_url()`, чтобы использовать `crud.create_db_url()`:

```python linenums="1"
# shortener_app/main.py

# ...

from . import crud, models, schemas


# ...

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return db_url
```

Во-первых, удалите импорт модуля `secrets`. Поскольку в `main.py` вы не используете `secrets` напрямую,
то и импортировать модуль в `main.py` не нужно.

В строке 14 вызывается `crud.create_db_url()`. Вы получаете объект базы данных `db_url` и можете использовать его поля
`db_url.key` и `db_url.secret_key` в строках 15 и 16.

Далее воспользуйтесь созданием `get_db_url_by_key()` и обновите `forward_to_target_url()`:

```python
# shortener_app/main.py

# ...

@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
```

В строке 11 вы обновляете `forward_to_target_url()`, чтобы использовать `crud.get_db_url_by_key()`. Это отличный шанс
использовать выражение присваивания `:=` и оптимизировать оператор `if`.

Оператор `:=` в просторечии называют `оператором моржа`, и он предоставляет новый синтаксис для присваивания
переменных в середине выражений.

Если `db_url` - это запись в базе данных, то в строке 12 возвращается `RedirectResponse` на `target_url`.
В противном случае в строке 14 вызывается `raise_not_found()`.

После всех этих обновлений пришло время проверить, работает ли ваш сокращатель URL так, как ожидалось. Перейдите
на сайт http://127.0.0.1:8000/docs и попробуйте использовать конечные точки API в браузере.

Ваш API функционирует так же, как и в конце предыдущего шага. Но теперь ваш код стал намного чище.

Тем не менее, вы не возвращаете URL, как можно было бы предположить по атрибутам `.url` и `.admin_url`. Вместо этого
возвращаются только ключи. Создание правильных URL будет рассмотрено в следующем разделе, где также будет добавлена
функциональность, позволяющая пользователям управлять своими сокращенными URL.

---

[Вернуться][main]

---

[main]: ../../README.md "содержание"

[506]: https://peps.python.org/pep-0506/ "506"
