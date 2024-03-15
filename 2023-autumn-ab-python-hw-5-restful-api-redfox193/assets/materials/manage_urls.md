[Вернуться][main]

# Управление URL-адресами

В предыдущем разделе вы очистили свой код, создав новые файлы и функции. Теперь вы будете развивать свои улучшения. В
конце этого шага вы сможете управлять URL-адресами, обращаясь к защищенным конечным точкам вашего API.

---

## Получение информации о вашем URL

При создании сокращенного URL-адреса в теле ответа появляется информация, которая выглядит следующим образом:

```json
{
  "target_url": "https://edu.tinkoff.ru/",
  "is_active": true,
  "clicks": 0,
  "url": "8RLNU",
  "admin_url": "8RLNU_VBM653H7"
}
```

В этом разделе мы создадим конечную точку администратора, чтобы впоследствии также видеть эту информацию о своем URL.
Эта конечная точка будет доступна только тем пользователям, которые знают ключ `secret_key`.

Начните с создания функции `get_db_url_by_secret_key()` в файле `crud.py`:

```python
# shortener_app/crud.py

# ...

def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )
```

Функция `get_db_url_by_secret_key()` проверяет вашу базу данных на наличие активной записи в базе данных с указанным
secret_key. Если запись в базе данных найдена, то вы возвращаете эту запись. В противном случае возвращается `None`.

Работа с возвращенными данными осуществляется в функции `get_url_info()` в файле `main.py`:

```python
# shortener_app/main.py

# ...

@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(
        secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        db_url.url = db_url.key
        db_url.admin_url = db_url.secret_key
        return db_url
    else:
        raise_not_found(request)
```

В строке 5 вы определяете новую конечную точку API по адресу `/admin/{secret_key}` URL.
Вы также даете этой конечной точке имя "administration info", чтобы было проще ссылаться на нее в дальнейшем.
В качестве `response_model` в строке 8 ожидается схема `URLInfo`.

После получения записи базы данных `crud.get_db_url_by_secret_key()` в строке 13, вы присваиваете ее `db_url`
и сразу же проверяете ее. Вы используете выражение присваивания для оператора if этой строки.

Но подождите секунду! Вам не кажется, что строки 14 и 15 выглядят знакомыми? Это именно те строки кода, которые вы
написали в `create_url()`, так что у вас есть шанс провести сеанс рефакторинга в том же файле:

```python
# shortener_app/main.py

# ...

from starlette.datastructures import URL

# ...

from .config import get_settings


# ...

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

# ...
```

В функции `get_admin_info()` вы делаете еще один шаг вперед, не ограничиваясь получением атрибутов `.url`
и `.admin_url`.
Вы также используете класс `URL` из пакета `starlette`, поставляемого с `FastAPI`. Чтобы создать `base_url` в строке 14,
вы передаете `base_url` из ваших настроек для инициализации класса `URL`. После этого можно использовать метод
`.replace()` для построения полного `URL`.

Раньше вы возвращали только `key` и `secret_key` сами по себе. Если вы хотели посетить одну из конечных точек, то должны
были сами добавить ее в свой базовый URL.

Теперь ваше приложение стало намного удобнее, поскольку функция `URLInfo` возвращает полные URL как для пересылающего
`url`, так и для `admin_url`.

С помощью этой функции можно обновить как `create_url()`, так и `get_url_info()`:

```python
# shortener_app/main.py

# ...

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


# ...

@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(
        secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)
```

Удалите строки, в которых задаются атрибуты `.url` и `.admin_url`. Вместо возврата `db_url` теперь возвращается схема
`URLInfo` из `get_admin_info()` в строках 10 и 24.

Вы очистили `create_url()` и получили конечную точку для просмотра информации о вашем URL.
Попробуйте использовать ее в браузере.
Теперь в ответе вы получаете полные URL вашего URL пересылки и URL администрирования:

```json
{
  "target_url": "https://edu.tinkoff.ru/",
  "is_active": true,
  "clicks": 0,
  "url": "http://127.0.0.1:8000/XV32M",
  "admin_url": "http://127.0.0.1:8000/admin/XV32M_LN78E2I7"
}
```

Пока все выглядит хорошо. Возможно, вы поделились сокращенным URL в своей сети. Но, несмотря на то, что на URL-адресе
многократно щелкали, значение clicks по-прежнему равно 0. В следующем разделе будет реализована функциональность для
просмотра частоты посещения вашего URL-адреса.

---

## Обновление количества посетителей

При посещении конечной точки "administration info" тело ответа содержит данные о вашем сокращенном URL. Одним из
параметров тела ответа является частота нажатий на ваш сокращенный URL. До сих пор этот показатель оставался нулевым.

Чтобы подсчитать количество кликов при посещении сокращенного URL, добавьте в файл `crud.py` новую функцию:

```python
# shortener_app/crud.py

# ...

def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url
```

Функция `update_db_clicks()` в строке 5 принимает в качестве аргумента `db_url`. Это означает, что внутри функции можно
ожидать существующую запись в базе данных. В строке 6 происходит увеличение значения `clicks` на единицу. С помощью
методов `.commit()` и `.refresh()` в строках 7 и 8 обновление сохраняется в базе данных.

> Примечание:
>
> Методы `.commit()` и `.refresh()` относятся к `db`, а не к `db_url`.

При переадресации на целевой URL вызывается только что созданная функция `update_db_clicks()`. Поэтому необходимо
настроить функцию `forward_to_target_url()` в файле `main.py`:

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
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

# ...
```

Вставьте вызов функции `crud.update_db_clicks()` в строку 12. Каждый раз, когда пользователь
использует ваш сокращенный URL-адрес, количество щелчков увеличивается.
По количеству щелчков можно судить о частоте посещения ссылки.

В какой-то момент вы можете решить удалить URL пересылки.

---

## Удаление URL

Приложение для сокращения URL-адресов Python отлично подходит для обмена ссылками с друзьями. После того как ваши друзья
перешли по ссылке, вы можете захотеть снова удалить сокращенный URL.

Как и в случае с функцией `update_db_clicks()`, начните с создания новой функции в файле `crud.py`:

```python
# shortener_app/crud.py

# ...

def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
```

Во-первых, обратите внимание, что называется функция `deactivate_db_url_by_secret_key()`, а не
`delete_db_url_by_secret_key()`. Следовательно, в строке 8 атрибут `.is_active` устанавливается в значение `False`, а не
удаляется полностью.

Помните, что в запросах к базе данных, где запрашивался объект URL, содержался фильтр, согласно которому URL должен быть
активным. Это означает, что все деактивированные URL не будут возвращены при обращении к базе данных. Для пользователя
это будет выглядеть так, как будто URL был удален, но только вы, как супер-администратор, можете выполнить действие по
удалению. Преимущество этого способа заключается в том, что вы можете восстановить деактивированный URL, если
пользователь передумал отключать свой URL.

Функция `deactivate_db_url_by_secret_key()` в строке 5 принимает в качестве аргумента ключ `secret_key`.
Этот секретный_ключ знает только создатель сокращенного URL.
Это отличная мера безопасности, когда только создатель может деактивировать URL.

Теперь единственная функция, которой не хватает, - это конечная точка для вызова `deactivate_db_url_by_secret_key()`.
Откройте `main.py` и добавьте функцию `delete_url()`:

```python
# shortener_app/main.py

# ...

@app.delete("/admin/{secret_key}")
def delete_url(
        secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)
```

В строке 5 используется декоратор `@app.delete()`, указывающий на то, что `delete_url()` принимает запросы `DELETE`.
Однако это действие по удалению разрешено только в том случае, если тело запроса содержит соответствующий `secret_key`.
Этот `secret_key` должен быть частью URL, как показано в строке 5, и являться аргументом функции `delete_url()`,
которую вы определяете в строке 6.

Тело функции `delete_url()`, вероятно, уже знакомо. Вы используете выражение присваивания `:=` в строке 9, чтобы
присвоить
`db_url` значение, возвращаемое функцией `crud.deactivate_db_url_by_secret_key()` в строке 10. Если запись в базе данных
с
указанным `secret_key` существует и была деактивирована, то в строке 11 возвращается сообщение об успехе. В противном
случае в строке 13 вызывается функция `raise_not_found()`.

Теперь вы также можете деактивировать URL-адреса, которые больше не нужны.
Создайте короткий URL с помощью сокращателя URL:

```json
{
  "target_url": "https://edu.tinkoff.ru/",
  "is_active": true,
  "clicks": 0,
  "url": "http://127.0.0.1:8000/PNYQ6",
  "admin_url": "http://127.0.0.1:8000/admin/PNYQ6_YCUM4RX7"
}
```

Когда сокращенный URL активен, он переадресует вас на целевой URL. Но как только вы деактивируете сокращенный URL,
переадресация на целевой URL больше не будет работать. 

```json
{
  "detail": "URL 'http://127.0.0.1:8000/PNYQ6' doesn't exist"
}
```

Прекрасно, это означает, что вы создали полнофункциональный сокращатель URL!

---

[Вернуться][main]

---

[main]: ../../README.md "содержание"

