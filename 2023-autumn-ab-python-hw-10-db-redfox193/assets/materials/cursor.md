[Вернуться][main]

---

# Курсор

Вместо того чтобы сразу выполнять весь запрос, есть возможность настроить курсор, инкапсулирующий запрос, и затем
получать результат запроса по несколько строк за раз. Одна из причин так делать заключается в том, чтобы избежать
переполнения памяти, когда результат содержит большое количество строк.

В PL/pgSQL:

```postgresql
name [ [ NO ] SCROLL ] CURSOR [ ( arguments ) ] FOR query;

DECLARE
    curs1 refcursor;
curs2 CURSOR FOR
SELECT *
FROM tenk1;
curs3 CURSOR (key integer) FOR
SELECT *
FROM tenk1
WHERE unique1 = key;
```

### Открытие курсора

```postgresql
OPEN unbound_cursorvar [ [ NO ] SCROLL ] FOR query;

OPEN curs1 FOR
SELECT *
FROM foo
WHERE key = mykey;
OPEN curs2;
```

### Открытие курсора на EXECUTE

```postgresql
OPEN unbound_cursorvar [ [ NO ] SCROLL ] FOR
EXECUTE query_string [ USING expression [, ... ] ];

OPEN curs1 FOR
EXECUTE 'SELECT * FROM ' || quote_ident(tabname)
    || ' WHERE col1 = $1' USING keyvalue;
```

### Передача параметров в курсор

```postgresql
DECLARE
    -- Переменная обязательно вводится до курсора
    key integer;
curs4 CURSOR FOR
SELECT *
FROM tenk1
WHERE unique1 = key;
curs3 CURSOR (key integer) FOR
SELECT *
FROM tenk1
WHERE unique1 = key;
BEGIN
key := 42;
OPEN curs4;
OPEN curs3(42);
```

Если необходимо освободить ресурсы до завершения транзакции или освободить переменную курсора для повторного открывания,
можно закрыть уже открытый курсор:

```postgresql
CLOSE cursor;

CLOSE curs1;
```

## Использование курсоров

### FETCH

FETCH извлекает строку из курсора в заданный таргет.

```postgresql
FETCH [ direction { FROM | IN } ] cursor INTO target;
```

В качестве direction могут использоваться: NEXT, FIRST, LAST, ABSOLUTE count, RELATIVE count и т.д.

```postgresql
FETCH curs1 INTO rowvar;
FETCH curs2 INTO foo, bar, baz;
FETCH LAST FROM curs3 INTO x, y;
FETCH RELATIVE -2 FROM curs4 INTO x;
```

Как это сделать с помощью Python:

```python
# Открывание курсора для работы с базой
cur = conn.cursor()
# Отправка запроса в базу
cur.execute("select 'Hello, world!', 6 * 7")
# Получение одной строки с результатом запроса
print(cur.fetchone())
conn.close()
```

Не забываем закрывать соединение!
**Connection** - это ресурс, который может и закончиться.
В этом нам помогут контекстные менеджеры.

## Контекстные менеджеры

### Создание таблиц

Инициализируем словарь с параметрами подключения:

```python
params = dict(
    database=environ['POSTGRES_DB'],
    user=environ['POSTGRES_USER'],
    password=environ['POSTGRES_PASSWORD'],
    host="localhost",
    port=15432,
)
```

Создадим ещё одну схему для сегодняшнего семинара

```python
def create_target(params):
    with connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('DROP SCHEMA IF EXISTS seminar_10 cascade;')
        cur.execute('CREATE SCHEMA seminar_10;')

        cur.execute('''
            CREATE TABLE seminar_10.user_types (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255)
            )
        ''')
        cur.execute('''
            CREATE TABLE seminar_10.users (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                active BOOLEAN,
                profile INTEGER,
                FOREIGN KEY(profile) REFERENCES seminar_10.user_types(id)
            )
        ''')
```

Функции для обогащения таблиц данными:

```python
def add_user_types(cur):
    cur.execute('''INSERT INTO seminar_10.user_types(name) VALUES ('Student')''')
    cur.execute('''INSERT INTO seminar_10.user_types(name) VALUES ('Teacher')''')


def add_teachers(cur):
    cur.execute('''
        INSERT INTO seminar_10.users (first_name, last_name, active, profile)
        VALUES ('Maxim', 'Popov', '1', 
               (SELECT id FROM seminar_10.user_types WHERE name = 'Teacher'))''')
    cur.execute('''
        INSERT INTO seminar_10.users (first_name, last_name, active, profile)
        VALUES ('Igor', 'Orlov', '1', 
               (SELECT id FROM seminar_10.user_types WHERE name = 'Teacher'))''')


def add_students(cur):
    cur.execute('''
        INSERT INTO seminar_10.users (first_name, last_name, active, profile)
        VALUES ('Ivan', 'Ivanov', '0', 
               (SELECT id FROM seminar_10.user_types WHERE name = 'Student'))''')
    cur.execute('''
        INSERT INTO seminar_10.users (first_name, last_name, active, profile)
        VALUES ('Petr', 'Petrov', '0', 
               (SELECT id FROM seminar_10.user_types WHERE name = 'Student'))''')
    cur.execute('''
        INSERT INTO seminar_10.users (first_name, last_name, active, profile)
        VALUES ('Petr', 'Sidorov', '0', 
               (SELECT id FROM seminar_10.user_types WHERE name = 'Student'))''')
```

### Выполнение запросов к БД

Запишем данные в таблицы:

```python
def insert_data(params):
    with connect(**params) as conn:
        cursor = conn.cursor()
        add_user_types(cursor)
        add_teachers(cursor)
        add_students(cursor)
```

Выборка всех студентов:

```python
def select_all_students(conn):
    query = '''SELECT first_name, last_name 
                 FROM seminar_10.users
                WHERE profile = (
                    SELECT id
                    FROM seminar_10.user_types
                    WHERE name = 'Student'
                )
    '''
    cur = conn.cursor()
    cur.execute(query)

    # Получить все строчки результата выполнения query
    # Это не всегда быстро, особенно если много результатов
    # Кроме того большое потребление памяти, так как возвращается list
    rows = cur.fetchall()

    # Как fetchall только задаем сколько хотим получить
    # rows = cur.fetchmany(10) 
    for row in rows:
        first_name, last_name = row
        print(first_name, last_name)


with connect(**params) as conn:
    select_all_students(conn)
```

Или итерируемся по объекту курсора:

```python
for row in cur:
    first_name, last_name = row
    print(first_name, last_name)
```

Перевод учителя Maxim Popov в студенты:

```python
with connect(**params) as conn:
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM seminar_10.users'
    )
    print(cur.fetchall())
```

```python
def alter_teacher(conn):
    cur = conn.cursor()
    cur.execute('''
        UPDATE seminar_10.users
           SET profile = (
                SELECT id
                FROM seminar_10.user_types
                WHERE name = 'Student'
            )
         WHERE first_name = 'Maxim'
           AND last_name = 'Popov'
    ''')


with connect(**params) as conn:
    alter_teacher(conn)
```

Параметризация запроса:

```python
def add_student(cur, first_name, last_name, active):
    query = """
        INSERT INTO seminar_10.users (first_name, last_name, active, profile)
        VALUES ('{}', '{}', '{}', 1)""".format(first_name, last_name, active)
    print(query)
    cur.execute(query)
```

Добавим студентов:

```python
with connect(**params) as conn:
    cur = conn.cursor()

    add_student(cur, 'Victor', 'Victorov', 1)
    add_student(cur, 'Sergey', 'Sergeev', 1)
    conn.commit()
```

Изучаем результат ...

## Проблема

![](../img/cursor/img.png)

https://www.psycopg.org/docs/usage.html#query-parameters

> WARNING!
>
> Никогда, никогда, НИКОГДА не используйте конкатенацию строк `(+)` или интерполяцию строковых параметров
> (форматирование `(%)`) в Python для передачи переменных в строку SQL-запроса. Даже под дулом пистолета.

Правильным способом передачи переменных в SQL-команде является использование второго аргумента метода `execute()`:

```python
SQL = 'INSERT INTO authors (name) VALUES (%s);'  # Note: no quotes
data = ("O'Reilly",)
cur.execute(SQL, data)  # Note: no % operator
```

## Изменение функции

```python
def add_student(cur, first_name, last_name, active):
    query = """
        INSERT INTO seminar_10.users (first_name, last_name, active, profile)
        VALUES (%s, %s, %s, 1)"""
    print(query)
    cur.execute(query, (first_name, last_name, active))
```

Проверяем:

```python
with connect(**params) as conn:
    cur = conn.cursor()

    add_student(cur, 'Anna', 'Chernova', True)
    conn.commit()

with connect(**params) as conn:
    select_all_students(conn)
```

---

[Вернуться][main]


[main]: ../../README.md "содержание"
