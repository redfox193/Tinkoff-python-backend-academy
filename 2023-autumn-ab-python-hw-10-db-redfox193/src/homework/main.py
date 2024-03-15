from dataclasses import dataclass, asdict

import psycopg2
from psycopg2 import OperationalError, ProgrammingError, connect
from os import environ
from dotenv import load_dotenv

load_dotenv(dotenv_path='../../docker/.env')


@dataclass
class ConnectionData:
    database: str
    user: str
    password: str
    host: str = "127.0.0.1"
    port: int = 15432


def create_connection(connection_data: ConnectionData):
    connection = None
    try:
        connection = connect(**asdict(connection_data))
        print('Connection to PostgreSQL DB successful')
    except (OperationalError, ProgrammingError) as e:
        print(f'''The error '{e}' while creating connection occurred''')
    return connection


def create_cursor(connection):
    cursor = None
    try:
        cursor = connection.cursor()
    except (OperationalError, ProgrammingError) as e:
        print(f'''The error '{e}' while creating cursor occurred''')
        raise
    return cursor


def execute_query(connection, query: str, query_data: list = None, autocommit=True,
                  success_message='Query executed successfully') -> None:
    try:
        connection.autocommit = autocommit
        cursor = create_cursor(connection)
        if query_data is not None:
            cursor.execute(query, query_data)
        else:
            cursor.execute(query)
        print(success_message)
    except (OperationalError, ProgrammingError, psycopg2.errors.CheckViolation) as e:
        print(f'''The error '{e}' occurred''')
    if not autocommit:
        connection.commit()


def execute_read_query(connection, query, query_data: list = None) -> list[tuple] | None:
    try:
        cursor = create_cursor(connection)
        if query_data is not None:
            cursor.execute(query, query_data)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except (OperationalError, ProgrammingError, psycopg2.errors.CheckViolation) as e:
        print(f'''The error '{e}' occurred''')


def create_tables(connection) -> None:
    create_users_table = '''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL CHECK (age >= 17 AND age <= 100),
            course INTEGER NOT NULL CHECK (course >= 1 AND course <= 4),
            specialty TEXT NOT NULL CHECK (
                specialty IN ('informatics', 'applied_informatics', 'applied_mathematics', 'cybersecurity')
            )
        );
    '''
    execute_query(connection, create_users_table, success_message="Table students was created successfully")


def insert_students(connection) -> None:
    students = [
        ('Sergey Smith', 18, 4, 'informatics'),
        ('Anna Johnson', 20, 3, 'applied_informatics'),
        ('Max Williams', 22, 3, 'applied_mathematics'),
        ('Lena Davis', 19, 2, 'cybersecurity'),
        ('John Brown', 21, 2, 'informatics'),
        ('Emily Miller', 19, 1, 'applied_informatics'),
        ('Michael Wilson', 20, 3, 'applied_mathematics'),
        ('Sophie Moore', 22, 2, 'cybersecurity'),
        ('Daniel Taylor', 18, 1, 'informatics'),
        ('Olivia Anderson', 20, 4, 'applied_informatics'),
        ('Benjamin White', 21, 3, 'applied_mathematics'),
        ('Ava Harris', 19, 4, 'cybersecurity')
    ]
    students_records = ', '.join(['%s'] * len(students))
    insert_query = (
        f'INSERT INTO students (name, age, course, specialty) VALUES {students_records}'
        f' ON CONFLICT (name) DO NOTHING;'
    )
    execute_query(connection, insert_query, query_data=students,
                  success_message="Table was filled with students successfully")


def update_age_by_id(connection, student_id: int, new_age: int) -> None:
    update_query = '''
        UPDATE students
        SET age = %s
        WHERE id = %s;
    '''
    update_data = [new_age, student_id]
    execute_query(connection, update_query, query_data=update_data,
                  success_message=f"Age for student with ID {student_id} changed successfully")


def delete_students_by_course(connection, course: int) -> None:
    delete_query = '''
        DELETE FROM students
        WHERE course = %s;
    '''
    delete_data = [course]
    execute_query(connection, delete_query, query_data=delete_data,
                  success_message=f"Student(-s) with course '{course}' deleted successfully")


def select_by_specialty(connection, specialty: str) -> list[tuple] | None:
    select_query = '''
        SELECT name, age, course, specialty FROM students
        WHERE specialty = %s;
    '''
    select_data = [specialty]
    students = execute_read_query(connection, select_query, query_data=select_data)
    return students


def complicated_query(connection, age: int) -> list[tuple] | None:
    query = '''
        SELECT specialty, COUNT(*) AS student_count
        FROM students
        WHERE age >= %s
        GROUP BY specialty
        ORDER BY student_count ASC, specialty ASC;
    '''
    query_data = [age]
    result = execute_read_query(connection, query, query_data=query_data)
    return result


def select_sorted_by_column(connection, column: str, asc=True) -> list[tuple] | None:
    sort_order = 'ASC' if asc else 'DESC'
    query = f'''
        SELECT *
        FROM students
        ORDER BY {column} {sort_order};
    '''
    result = execute_read_query(connection, query)
    return result


def group_by_column(connection, column: str) -> list[tuple] | None:
    query = f'''
        SELECT {column}, COUNT(*) AS count
        FROM students
        GROUP BY {column};
    '''
    query_data = [column]
    result = execute_read_query(connection, query, query_data=query_data)
    return result


def select_by_name(connection, name: str) -> list[tuple]:
    select_query = '''
        SELECT * FROM students
        WHERE name = %s;
    '''
    select_data = [name]
    students = execute_read_query(connection, select_query, query_data=select_data)
    return students


def insert_new_student(connection, name: str, age: int, course: int, specialty: str) -> None:
    query = '''
        INSERT INTO students (name, age, course, specialty)
        VALUES (%s, %s, %s, %s);
    '''
    data = [name, age, course, specialty]
    execute_query(connection, query, query_data=data, success_message="New student inserted successfully")


def print_records(records: list[tuple] | None, empty_message: str = "No records to print") -> None:
    if records is None or len(records) == 0:
        print(empty_message)
    else:
        for record in records:
            print(record)


def get_column_names(connection, query: str) -> list:
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.fetchall()

    column_names = [description[0] for description in cursor.description]
    return column_names


def main() -> None:
    connection_data = ConnectionData(
        database=environ['POSTGRES_DB'],
        user=environ['POSTGRES_USER'],
        password=environ['POSTGRES_PASSWORD']
    )
    connection = create_connection(connection_data)

    if connection is None:
        print("Can't proccess queries as connection wasn't established")
        return

    # 1. create table
    create_tables(connection)

    # 2. insert students
    insert_students(connection)
    students = execute_read_query(connection, "SELECT * FROM students")
    print_records(students, "Table is empty")

    # 3. update student's age by id
    student_id = int(input("Input id of the student to update:"))
    new_age = int(input("Input new age for this student:"))
    update_age_by_id(connection, student_id=student_id, new_age=new_age)
    student = execute_read_query(connection, f"SELECT * FROM students WHERE id = {student_id}")
    print_records(student, "Nobody was changed")

    # 4. delete students by course
    course = int(input("Input course to delete students from table:"))
    delete_students_by_course(connection, course=course)
    students = execute_read_query(connection, "SELECT * FROM students")
    print_records(students, "Table is empty")

    # 5. select students by specialty
    specialty = input("Select students by specialty:")
    students = select_by_specialty(connection, specialty=specialty)
    print_records(students, f"No students from specialty '{specialty}' was selected")

    # 6. complicated query
    print("Let's count students of each specialty from certain age and print ordered statistic")
    age = int(input("Input minimum age for students to count:"))
    records = complicated_query(connection, age=age)
    print_records(records, f"No students of age >= {age} or table is empty")

    column_names = get_column_names(connection, "SELECT * FROM students LIMIT 0")
    # 8.1 sort students by column
    print(f"Let's get our students sorted by certain column: {column_names}")
    column = input("Column name:")
    order = input("In ASC order? (y/n):")
    if order not in ('y', 'n'):
        print("Unknown answer, query was skipped")
    else:
        if order == 'n':
            students = select_sorted_by_column(connection, column=column, asc=False)
        else:
            students = select_sorted_by_column(connection, column=column)
        print_records(students, "Nobody was selected")

    # 8.2 group students by different column
    print(f"Let's group our students by certain column and count them: {column_names}")
    column = input("Column name:")
    records = group_by_column(connection, column)
    print_records(records, "No records to print")

    # 8.3 select student by name
    name = input("Select student by name:")
    students = select_by_name(connection, name=name)
    print_records(students, f"No students with full name '{name}'")

    # 8.4 insert new student
    print("Let's insert new student")
    name = input("name:")
    age = int(input("age(>=17, <=100):"))
    course = int(input("course(>=1, <=4):"))
    specialty = input("specialty('informatics', 'applied_informatics', 'applied_mathematics', 'cybersecurity'):")
    insert_new_student(connection, name=name, age=age, course=course, specialty=specialty)
    student = select_by_name(connection, name)
    print_records(student, "Student wasn't added")


if __name__ == '__main__':
    main()
