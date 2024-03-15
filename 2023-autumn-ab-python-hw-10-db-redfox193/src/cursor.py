from psycopg2 import OperationalError, ProgrammingError, connect
from os import environ
from dotenv import load_dotenv

load_dotenv(dotenv_path='../docker/.env')


def create_connection(db_name, db_user, db_password, db_host='127.0.0.1', db_port=15432):
    connection = None
    try:
        connection = connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print('Connection to PostgreSQL DB successful')
    except (OperationalError, ProgrammingError) as e:
        print(f'''The error '{e}' occurred''')
    return connection


def fetch_one_row(conn):
    # Открытие курсора для работы с базой
    cur = conn.cursor()
    # Отправка запроса в базу
    cur.execute('''select * from information_schema.tables''')
    # Получение одной строки с результатом запроса
    print(cur.fetchone())
    conn.close()


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


def insert_data(params):
    with connect(**params) as conn:
        cursor = conn.cursor()
        add_user_types(cursor)
        add_teachers(cursor)
        add_students(cursor)


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


def add_student(cur, first_name, last_name, active):
    query = '''
        INSERT INTO seminar_10.users (first_name, last_name, active, profile)
        VALUES ('{}', '{}', '{}', 1)
    '''.format(first_name, last_name, active)
    print(query)
    cur.execute(query)


# def add_student(cur, first_name, last_name, active):
#     query = """
#         INSERT INTO seminar_10.users (first_name, last_name, active, profile)
#         VALUES (%s, %s, %s, 1)
#     """
#     print(query)
#     cur.execute(query, (first_name, last_name, active))


def main():
    connection = create_connection(
        db_name=environ['POSTGRES_DB'],
        db_user=environ['POSTGRES_USER'],
        db_password=environ['POSTGRES_PASSWORD'],
    )
    # fetch_one_row(connection)

    params = dict(
        database=environ['POSTGRES_DB'],
        user=environ['POSTGRES_USER'],
        password=environ['POSTGRES_PASSWORD'],
        host='localhost',
        port=15432,
    )

    # create_target(params)
    # insert_data(params)

    # with connect(**params) as conn:
    #     select_all_students(conn)

    # with connect(**params) as conn:
    #     cur = conn.cursor()
    #     cur.execute(
    #         'SELECT * FROM seminar_10.users'
    #     )
    #     print(cur.fetchall())
    #
    # with connect(**params) as conn:
    #     alter_teacher(conn)
    #
    # with connect(**params) as conn:
    #     select_all_students(conn)

    # with connect(**params) as conn:
    #     cur = conn.cursor()
    #
    #     add_student(cur, 'Victor', 'Victorov', 1)
    #     add_student(cur, 'Sergey', 'Sergeev', 1)
    #     conn.commit()

    # with connect(**params) as conn:
    #     select_all_students(conn)

    # with connect(**params) as conn:
    #     cur = conn.cursor()
    #
    #     add_student(cur, 'Anna', 'Chernova', True)
    #     conn.commit()
    #
    # with connect(**params) as conn:
    #     select_all_students(conn)


if __name__ == '__main__':
    main()
