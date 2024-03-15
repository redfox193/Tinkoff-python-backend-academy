[Вернуться][main]

---

# ORM

## Суть ORM

**ORM** (Object-Relational Mapping) — технология программирования, которая связывает базы данных с концепциями
объектно-ориентированных языков программирования, создавая «виртуальную объектную базу данных». Существует множество
вариантов реализации этой технологии.

### Задача

Необходимо обеспечить работу с данными в терминах классов, а не таблиц данных и напротив, преобразовать термины и данные
классов в данные, пригодные для хранения в СУБД. Необходимо также обеспечить интерфейс для CRUD-операций над данными. В
общем, необходимо избавиться от необходимости писать SQL-код для взаимодействия в СУБД.

### Решение

Решение проблемы хранения существует — это реляционные СУБД. Но их использование для хранения объектно-ориентированных
данных приводит к семантическому разрыву, заставляя программистов писать программное обеспечение, которое должно уметь
как обрабатывать данные в объектно- ориентированном виде, так и уметь сохранить эти данные в реляционной
форме.Разработано множество пакетов, устраняющих необходимость в преобразовании объектов для хранения в реляционных
базах данных.

С точки зрения программиста система должна выглядеть как постоянное хранилище объектов. Он может просто создавать
объекты и работать с ними как обычно, а они автоматически будут сохраняться в реляционной базе данных.

## Peewee

[peewee][peewee] - a small, expressive orm -- supports postgresql, mysql, sqlite and cockroachdb

```shell
pip install peewee
```

```python
from peewee import PostgresqlDatabase

params = dict(
    database=environ['POSTGRES_DB'],
    user=environ['POSTGRES_USER'],
    password=environ['POSTGRES_PASSWORD'],
    host='localhost',
    port=15432,
)

db = PostgresqlDatabase(**params)
```

Опишем данные в виде класса:

```python
from peewee import Model, CharField, DateField, BooleanField


class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db  # модель будет использовать базу данных 'postgres'
        schemaname = 'seminar_10'
```

Другие типы полей - [peewee field types][peewee field types]

Инициализирующие аргументы:

- *null=False* – возможно ли хранение null-значений;
- *index=False* – создавать ли индекс для данного столбца в базе;
- *unique=False* – создавать ли уникальный индекс для данного столбца в базе.
- *verbose_name=None* – строка для человекопонятного представления поля;
- *help_text=None* – строка с вспомогательным текстом для поля;
- *db_column=None* – строка, явно задающая название столбца в базе для данного поля, используется например при работе с
  legacy-базой данных;
- *default=None* – значение по умолчанию для полей класса при инстанцировании;
- *choices=None* – список или кортеж двухэлементных кортежей, где первый элемент – значение для базы, второй –
  отображаемое значение (аналогично джанге);
- *primary_key=False* – использовать ли данное поле, как первичный ключ;

Ещё одна сущность:

```python
class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField(null=False)
    animal_type = CharField()

    #     is_wild = BooleanField(null=True)

    class Meta:
        database = db
        schemaname = 'seminar_10'
```

Создание таблицы в БД со всеми необходимыми колонками, ключами и сиквенсами (если они нужны)

```python
Person.create_table()
Pet.create_table()
```

## Взаимодействие с БД

Добавим данные:

```python
from datetime import date


def add_persons():
    uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
    uncle_bob.save()  # cохранение Боба в БД

    grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)
    herb = Person.create(name='Herb', birthday=date(1950, 5, 5), is_relative=False)

    grandma.name = 'Grandma L.'

    grandma.save()  # обновление записи grandma

    Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
    Pet.create(owner=herb, name='Fido', animal_type='dog')
    Pet.create(owner=herb, name='Mittens', animal_type='cat')
    Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')
```

Считаем данные grandma:

```python
def get_grandma():
    grandma = Person.select().where(Person.name == 'Grandma L.').get()
    print(grandma.name)

    grandma = Person.get(Person.name == 'Grandma L.')
    print(grandma.name)
```

Все персоны:

```python
def get_all_persons():
    for person in Person.select():
        print(person.name, person.is_relative)
```

Посчитаем питомцев каждой персоны:

```python
def get_persons_pets():
    for person in Person.select():
        print(person.name, person.pets.count(), 'pets')
        for pet in person.pets:
            print(' ', pet.name, pet.animal_type)
```

Внесём изменения:

```python
def change_data():
    uncle_bob = Person.select().where(Person.name == 'Bob').get()
    herb_mittens = Pet.select().where(Pet.name == 'Mittens').get()
    herb_fido = Pet.select().where(Pet.name == 'Fido').get()

    herb_mittens.delete_instance()
    herb_fido.owner = uncle_bob
    herb_fido.save()
```

Фильтр значений:

```python
def filter_data():
    query = Pet.select().where(Pet.animal_type == 'cat')
    for pet in query:
        print(pet.name, pet.owner.name)
```

Объединение данных:

```python
def join_data():
    query = (Pet
             .select(Pet, Person)
             .join(Person)
             .where(Pet.animal_type == 'cat'))

    for pet in query:
        print(pet.name, pet.owner.name)
    print('---')
    for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
        print(pet.name)
```

Сортировка данных:

```python
def sort_data():
    for person in Person.select().order_by(Person.birthday.desc()):
        print(person.name)
```

Использование сложных условий в запросах:

```python
def complex_cond():
    d1940 = date(1940, 1, 1)
    d1960 = date(1960, 1, 1)
    query = (Person
             .select()
             .where((Person.birthday < d1940) | (Person.birthday > d1960)))

    for person in query:
        print(person.name, person.birthday)
    print('---')
    query = (Person
             .select()
             .where(Person.birthday.between(d1940, d1960)))

    for person in query:
        print(person.name, person.birthday)
```

Объдинение нескольких таблиц:

```python
from peewee import JOIN, fn


def complex_join():
    query = (Person
             .select(Person, fn.COUNT(Pet.id).alias('pet_count'))
             .join(Pet, JOIN.LEFT_OUTER)  # не исключение людей без животных
             .group_by(Person)
             .order_by(Person.name))

    for person in query:
        print(person.name, person.pet_count, 'pets')
```

Удаление данных:

```python
def drop_data():
    models = (Person, Pet)

    db.drop_tables(models)
    db.close()
```

## ORM: плюсы и минусы

ORM, по идее, должен избавить нас от написания SQL запросов и, в идеале, вообще абстрагировать от базы данных (от
способа хранения данных), чтобы мы могли работать с классами, в той или иной степени выражающими объекты бизнес-логики,
не задаваясь вопросом, в каких таблицах всё это по факту лежит.

Для примера возьмем две таблицы: книги и авторы книг, отношение многие ко многим (у книг может быть много авторов, у
авторов может быть много книг). Т.е. в базе это будут `books`, `authors` и связующая таблица `author_book`:

```postgresql
CREATE TABLE authors
(
    id   serial,
    name varchar(1000) not null,
    PRIMARY KEY (id)
);

CREATE TABLE books
(
    id   serial,
    name VARCHAR(1000) not null,
    text text          not null,
    PRIMARY KEY (id)
);

CREATE TABLE author_book
(
    author_id bigint REFERENCES authors (id),
    book_id   bigint REFERENCES books (id),
    PRIMARY KEY (author_id, book_id)
);
```

### Кейс 1: создание записей

- Pure SQL
  - Piece of cake. Простые CREATE и INSERT
  - Много писанины
  - Нужно знать синтаксис SQL
- ORM
  - Piece of cake. Создаём нужные классы, наполняем
  - Много писанины
  - Нужно разобраться с ORM

### Кейс 2: обновление записей

- Pure SQL
  - Piece of cake. Просто UPDATE
- ORM
  - Piece of cake. Пользуемся нужным методом (как с именем бабули ранее)

### Кейс 3: простая выборка

- Pure SQL
  - Piece of cake. Запрос с агрегацией:
    ```postgresql
       select
         b.id as book_id
         , b.name as book_name
         , json_agg(a.name) as authors
       from
         books b
       inner join
         author_book ab
           on b.id = ab.book_id
       inner join
         authors a
           on ab.author_id = a.id
       group by
         b.id;
    ```
- ORM
  - Piece of cake (так ли это?)
    - Проходим циклом и находим нужное
    - Будет несколько запросов: выборка всех книг и для каждой выборка автора
    - С ростом количества данных будет выполняться всё дольше
    - Вытянутся все поля, а не только нужные; придётся разбираться с SQL

### Кейс 4: сложное обновление

- Pure SQL
  - Piece of cake. Простой подзапрос:
    ```postgresql
      UPDATE authors
      SET name = 'Лев Толстой'
      WHERE id in (
          SELECT
            id
          FROM
            authors
          ORDER BY
            id DESC
          LIMIT 2 );
    ```
- ORM
  - Долгое изучение мануалов
  - Никаких подзапросов
  - Неоптимально с точки зрения БД

---

[Вернуться][main]

[main]: ../../README.md "содержание"

[peewee]: http://docs.peewee-orm.com/en/latest/ "peewee"

[peewee field types]: https://peewee.readthedocs.io/en/latest/peewee/models.html#field-types-table "peewee field types"
