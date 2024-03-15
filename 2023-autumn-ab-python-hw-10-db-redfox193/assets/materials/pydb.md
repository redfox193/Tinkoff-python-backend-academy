[Вернуться][main]

---

# Использование библиотек для взаимодействия с БД

## Подключение и создание БД

Прежде чем взаимодействовать с какой-либо базой данных с помощью библиотеки Python SQL, необходимо подключиться к ней.
Рассмотрим, как подключаться к БД PostgreSQL из приложения на Python.

[Python DB API 2.0][db pep] - стандарт интерфейсов для пакетов, работающих с БД

### Библиотека psycopg2

В Python нет стандартной SQL-библиотеки, которую можно было бы использовать для взаимодействия с
базой данных PostgreSQL. Вместо этого необходимо установить сторонний драйвер Python SQL для взаимодействия с
PostgreSQL. Одним из таких драйверов Python SQL для PostgreSQL является `psycopg2`. Для установки модуля psycopg2 Python
SQL выполните в терминале следующую команду:

```shell
pip install psycopg2-binary
```

Для установления соединения с базой данных PostgreSQL необходимо определить функцию `create_connection()`:

```python
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection
```

Для подключения к серверу PostgreSQL из приложения на языке Python используется функция `psycopg2.connect()`.

Затем можно использовать функцию `create_connection()` для создания соединения с базой данных PostgreSQL:

```python
connection = create_connection(
    db_name=environ['POSTGRES_DB'],
    db_user=environ['POSTGRES_USER'],
    db_password=environ['POSTGRES_PASSWORD'],
)
```

Далее необходимо создать базу данных `sm_app`. Можно определить функцию для выполнения любого SQL-запроса в PostgreSQL.
Ниже определена функция `create_database()` для создания новой базы данных на нашем локальном сервере PostgreSQL:

```python
def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


create_database_query = "CREATE DATABASE sm_app"
create_database(connection, create_database_query)
```

После выполнения приведенного выше скрипта на сервере баз данных PostgreSQL появится база данных `sm_app`.

## Создание таблиц

Рассмотрим, как создавать таблицы внутри БД.

Как уже говорилось ранее, мы создадим четыре таблицы:

- users
- posts
- comments
- likes

Объект соединения, возвращаемый функцией `psycopg2.connect()`, содержит объект курсора.
Для выполнения SQL-запросов на языке Python к базе данных PostgreSQL можно использовать функцию `cursor.execute()`.

Определим функцию `execute_query()`:

```python
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
```

С помощью этой функции можно создавать таблицы, вставлять записи, изменять записи и удалять записи в базе данных
PostgreSQL.

Теперь создадим таблицу `users` в базе данных `sm_app`:

```python
create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL, 
      age INTEGER,
      gender TEXT,
      nationality TEXT
    )
"""

execute_query(connection, create_users_table)
```

В запросе на создание таблицы users ключевое слово `SERIAL` используется для создания столбцов, которые увеличиваются
автоматически (автоинкремент).

Поскольку между пользователями и постами существует связь "один-ко-многим", в таблице `posts` можно увидеть внешний ключ
`user_id`, который ссылается на столбец `id` таблицы `users`.

Ссылки на внешние ключи также задаются как показано в следующем скрипте, создающем таблицу `posts`:

```python
create_posts_table = """
    CREATE TABLE IF NOT EXISTS posts (
      id SERIAL PRIMARY KEY, 
      title TEXT NOT NULL, 
      description TEXT NOT NULL, 
      user_id INTEGER REFERENCES users(id)
    )
"""

execute_query(connection, create_posts_table)
```

Для создания таблицы `comments` необходимо написать запрос `CREATE` для таблицы комментариев и передать его в функцию
`execute_query()`. Процесс создания таблицы `likes` аналогичен. Необходимо только модифицировать запрос `CREATE`, чтобы
создать таблицу лайков вместо таблицы комментариев.

## Вставка

Существует два способа вставки записей в базы данных из приложения на языке Python. В первом случае
используется строковый SQL-запрос, а во втором - `.executeemany()`. psycopg2 следует второму подходу, хотя `.execute()`
используется для выполнения запроса, основанного на плейсхолдерах, такой подход тоже иногда полезен.

В `.execute()` передается SQL-запрос с плейсхолдерами и список записей. Каждая запись в списке будет кортежем, где
значения кортежей соответствуют значениям столбцов в таблице базы данных. Вот как можно вставить записи о пользователях
в таблицу `users` в базе данных PostgreSQL:

```python
users = [
    ("James", 25, "male", "USA"),
    ("Leila", 32, "female", "France"),
    ("Brigitte", 35, "female", "England"),
    ("Mike", 40, "male", "Denmark"),
    ("Elizabeth", 21, "female", "Canada"),
]

user_records = ", ".join(["%s"] * len(users))

insert_query = (
    f"INSERT INTO users (name, age, gender, nationality) VALUES {user_records}"
)

connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query, users)
```

В приведенном выше скрипте создаётся список `users`, содержащий пять записей пользователей в виде кортежей. Далее
создается строка-плейсхолдер с пятью элементами-плейсхолдерами `(%s)`, которые соответствуют пяти записям пользователей.
Строка-плейсхолдер конкатенируется с запросом, который вставляет записи в таблицу `users`. Наконец, строка запроса и
записи пользователей передаются в `.execute()`.

Ещё один пример вставки записей в таблицу PostgreSQL. Следующий скрипт вставляет записи в таблицу `posts`:

```python
posts = [
    ("Happy", "I am feeling very happy today", 1),
    ("Hot Weather", "The weather is very hot today", 2),
    ("Help", "I need some help with my work", 2),
    ("Great News", "I am getting married", 1),
    ("Interesting Game", "It was a fantastic game of tennis", 5),
    ("Party", "Anyone up for a late-night party today?", 3),
]

post_records = ", ".join(["%s"] * len(posts))

insert_query = (
    f"INSERT INTO posts (title, description, user_id) VALUES {post_records}"
)

connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query, posts)
```

Аналогичным образом можно вставлять записи в таблицы комментариев и лайков.

## Выборка

Для выбора записей из таблицы PostgreSQL используется `cursor.execute()`, а затем `.fetchall()`.
Этот метод возвращает список кортежей, в котором каждый кортеж сопоставлен с соответствующей строкой
в извлеченных записях.

Для упрощения процесса можно создать функцию `execute_read_query()`.

### SELECT

Теперь выберем все записи из таблицы `users`:

```python
def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


select_users = "SELECT * FROM users"
users = execute_read_query(connection, select_users)

for user in users:
    print(user)
```

В приведённом выше скрипте запрос `SELECT` выбирает всех пользователей из таблицы `users`. Он передается в функцию
`execute_read_query()`, которая возвращает все записи из таблицы `users`. Затем записи обходятся и выводятся на консоль.

> **Примечание:**
>
> Не рекомендуется использовать `SELECT *` для больших таблиц, так как это может привести к большому
> количеству операций ввода-вывода, увеличивающих сетевой трафик и нагрузку на БД. **Никогда** не делайте так на проде!

Аналогичным образом можно получить все записи из таблицы posts с помощью приведенного ниже скрипта:

```python
select_posts = "SELECT * FROM posts"
posts = execute_read_query(connection, select_posts)

for post in posts:
    print(post)
```

### JOIN

Для получения данных из двух связанных таблиц можно также выполнять сложные запросы, включающие операции `JOIN`.
Например, следующий скрипт возвращает идентификаторы и имена пользователей, а также описание сообщений, которые эти
пользователи разместили:

```python
select_users_posts = """
    SELECT
      users.id,
      users.name,
      posts.description
    FROM
      posts
      INNER JOIN users ON users.id = posts.user_id
"""

users_posts = execute_read_query(connection, select_users_posts)

for users_post in users_posts:
    print(users_post)
```

Также можно выбрать данные из трёх связанных таблиц, реализовав несколько операторов `JOIN`. Следующий скрипт возвращает
все сообщения, а также комментарии к ним и имена пользователей, оставивших комментарии:

```python
select_posts_comments_users = """
    SELECT
      posts.description as post,
      text as comment,
      name
    FROM
      posts
      INNER JOIN comments ON posts.id = comments.post_id
      INNER JOIN users ON users.id = comments.user_id
"""

posts_comments_users = execute_read_query(
    connection, select_posts_comments_users
)

for posts_comments_user in posts_comments_users:
    print(posts_comments_user)
```

Из вывода видно, что имена столбцов не возвращаются функцией `.fetchall()`. Для возврата имён столбцов можно
использовать атрибут `.description` объекта курсора. Например, следующий список возвращает все имена столбцов для
приведенного выше запроса:

```python
cursor = connection.cursor()
cursor.execute(select_posts_comments_users)
cursor.fetchall()

column_names = [description[0] for description in cursor.description]
print(column_names)
```

### WHERE

Теперь выполним запрос `SELECT`, который вернёт сообщение вместе с общим количеством лайков, полученных этим сообщением:

```python
select_post_likes = """
    SELECT
      p.description as post,
      COUNT(l.id) as likes
    FROM
      likes l,
      posts p
    WHERE
      p.id = l.post_id
    GROUP BY
      l.post_id, p.description
"""

post_likes = execute_read_query(connection, select_post_likes)

for post_like in post_likes:
    print(post_like)
```

Используя предложение `WHERE` и агрегацию `GROUP BY`, мы можем возвращать более конкретные результаты.

## Обновление записей в таблице

В предыдущем разделе рассмотрели, как выбирать записи из БД. В этом разделе рассмотрим процесс обновления записей.

Обновление записей довольно простое. Для этого снова можно воспользоваться функцией `execute_query()`. В качестве
примера можно обновить описание сообщения с идентификатором `2`. Сначала выберем описание этого сообщения:

```python
select_post_description = "SELECT description FROM posts WHERE id = 2"

post_description = execute_read_query(connection, select_post_description)

for description in post_description:
    print(description)
```

Следующий скрипт обновляет описание:

```python
update_post_description = """
    UPDATE
      posts
    SET
      description = "The weather has become pleasant now"
    WHERE
      id = 2
"""

execute_query(connection, update_post_description)
```


## Удаление записей таблицы

Рассмотрим, как удалять записи в таблице с помощью Python SQL для БД PostgreSQL.

Мы снова можем использовать функцию `execute_query()` для удаления записей из БД. Для этого достаточно передать
в `execute_query()` объект соединения и строковый запрос для удаляемой записи. Затем `execute_query()` создаст объект
курсора, используя соединение, и передаст строковый запрос в `cursor.execute()`, что приведет к удалению записей.

В качестве примера попробуем удалить комментарий с идентификатором `5`:

```python
delete_comment = "DELETE FROM comments WHERE id = 5"
execute_query(connection, delete_comment)
```

Теперь, если выбрать все записи из таблицы комментариев, то можно увидеть, что пятый комментарий был удален.

---

[Вернуться][main]


[main]: ../../README.md "содержание"

[db pep]: https://www.python.org/dev/peps/pep-0249/ "db pep"
