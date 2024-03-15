from peewee import (
    PostgresqlDatabase,
    Model,
    CharField,
    DateField,
    BooleanField,
    ForeignKeyField,
    JOIN,
    fn,
)
from os import environ
from dotenv import load_dotenv
from datetime import date

load_dotenv(dotenv_path='../docker/.env')

params = dict(
    database=environ['POSTGRES_DB'],
    user=environ['POSTGRES_USER'],
    password=environ['POSTGRES_PASSWORD'],
    host='localhost',
    port=15432,
)

db = PostgresqlDatabase(**params)


class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db  # модель будет использовать базу данных 'postgres'
        schemaname = 'seminar_10'


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField(null=False)
    animal_type = CharField()
    is_wild = BooleanField(null=True)

    class Meta:
        database = db
        schemaname = 'seminar_10'


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


def get_grandma():
    grandma = Person.select().where(Person.name == 'Grandma L.').get()
    print(grandma.name)

    grandma = Person.get(Person.name == 'Grandma L.')
    print(grandma.name)


def get_all_persons():
    for person in Person.select():
        print(person.name, person.is_relative)


def change_data():
    uncle_bob = Person.select().where(Person.name == 'Bob').get()
    herb_mittens = Pet.select().where(Pet.name == 'Mittens').get()
    herb_fido = Pet.select().where(Pet.name == 'Fido').get()

    herb_mittens.delete_instance()
    herb_fido.owner = uncle_bob
    herb_fido.save()


def get_persons_pets():
    for person in Person.select():
        print(person.name, person.pets.count(), 'pets')
        for pet in person.pets:
            print(' ', pet.name, pet.animal_type)


def filter_data():
    query = Pet.select().where(Pet.animal_type == 'cat')
    for pet in query:
        print(pet.name, pet.owner.name)


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


def sort_data():
    for person in Person.select().order_by(Person.birthday.desc()):
        print(person.name)


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


def complex_join():
    query = (Person
             .select(Person, fn.COUNT(Pet.id).alias('pet_count'))
             .join(Pet, JOIN.LEFT_OUTER)  # не исключение людей без животных
             .group_by(Person)
             .order_by(Person.name))

    for person in query:
        print(person.name, person.pet_count, 'pets')


def drop_data():
    models = (Person, Pet)

    db.drop_tables(models)
    db.close()


def main():
    Person.create_table()
    Pet.create_table()

    # add_persons()

    # get_grandma()

    # get_all_persons()

    # get_persons_pets()

    # change_data()
    # get_persons_pets()

    # filter_data()
    # join_data()
    # sort_data()

    # complex_cond()

    # complex_join()

    # drop_data()


if __name__ == '__main__':
    main()
