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


# def create_database(connection, query):
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print('Query executed successfully')
#     except (OperationalError, ProgrammingError) as e:
#         print(f'''The error '{e}' occurred''')
#
#
# def execute_query(connection, query, autocommit=True):
#     if autocommit:
#         connection.autocommit = autocommit
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print('Query executed successfully')
#     except (OperationalError, ProgrammingError) as e:
#         print(f'''The error '{e}' occurred''')
#     if not autocommit:
#         connection.commit()
#
#
# def create_tables(connection):
#     create_users_table = '''
#         CREATE TABLE IF NOT EXISTS users (
#             id SERIAL PRIMARY KEY,
#             name TEXT NOT NULL,
#             age INTEGER,
#             gender TEXT,
#             nationality TEXT
#         )
#     '''
#     execute_query(connection, create_users_table)
#
#     create_posts_table = '''
#         CREATE TABLE IF NOT EXISTS posts (
#             id SERIAL PRIMARY KEY,
#             title TEXT NOT NULL,
#             description TEXT NOT NULL,
#             user_id INTEGER REFERENCES users(id)
#         )
#     '''
#     execute_query(connection, create_posts_table)
#
#     create_comments_table = '''
#         CREATE TABLE IF NOT EXISTS likes (
#             id SERIAL PRIMARY KEY,
#             user_id INTEGER REFERENCES users(id),
#             post_id INTEGER REFERENCES posts(id)
#         )
#     '''
#     execute_query(connection, create_comments_table)
#
#     create_likes_table = '''
#         CREATE TABLE IF NOT EXISTS comments (
#             id SERIAL PRIMARY KEY,
#             text text,
#             user_id INTEGER REFERENCES users(id),
#             post_id INTEGER REFERENCES posts(id)
#         )
#     '''
#     execute_query(connection, create_likes_table)
#
#
# def insert_users(connection):
#     users = [
#         ('James', 25, 'male', 'USA'),
#         ('Leila', 32, 'female', 'France'),
#         ('Brigitte', 35, 'female', 'England'),
#         ('Mike', 40, 'male', 'Denmark'),
#         ('Elizabeth', 21, 'female', 'Canada'),
#     ]
#     user_records = ', '.join(['%s'] * len(users))
#     insert_query = (
#         f'INSERT INTO users (name, age, gender, nationality) VALUES {user_records}'
#     )
#     connection.autocommit = True
#     cursor = connection.cursor()
#     cursor.execute(insert_query, users)
#     connection.autocommit = False
#
#
# def insert_posts(connection):
#     posts = [
#         ('Happy', 'I am feeling very happy today', 1),
#         ('Hot Weather', 'The weather is very hot today', 2),
#         ('Help', 'I need some help with my work', 2),
#         ('Great News', 'I am getting married', 1),
#         ('Interesting Game', 'It was a fantastic game of tennis', 5),
#         ('Party', 'Anyone up for a late-night party today?', 3),
#     ]
#
#     post_records = ', '.join(['%s'] * len(posts))
#
#     insert_query = (
#         f'INSERT INTO posts (title, description, user_id) VALUES {post_records}'
#     )
#
#     connection.autocommit = True
#     cursor = connection.cursor()
#     cursor.execute(insert_query, posts)
#     connection.autocommit = False
#
#
# def insert_comments_and_likes(connection):
#     comments = [
#         ('Count me in', 1, 6),
#         ('What sort of help?', 5, 3),
#         ('Congrats buddy', 2, 4),
#         ('I was rooting for Nadal though', 4, 5),
#         ('Help with your thesis?', 2, 3),
#         ('Many congratulations', 5, 4),
#     ]
#
#     likes = [
#         (1, 6),
#         (2, 3),
#         (1, 5),
#         (5, 4),
#         (2, 4),
#         (4, 2),
#         (3, 6),
#     ]
#
#     comments_records = ', '.join(['%s'] * len(comments))
#     likes_records = ', '.join(['%s'] * len(likes))
#
#     insert_comments_query = (
#         f'INSERT INTO comments (text, user_id, post_id) VALUES {comments_records}'
#     )
#     insert_likes_query = (
#         f'INSERT INTO likes (user_id, post_id) VALUES {likes_records}'
#     )
#
#     connection.autocommit = True
#     cursor = connection.cursor()
#     cursor.execute(insert_comments_query, comments)
#     cursor.execute(insert_likes_query, likes)
#     connection.autocommit = False
#
#
# def execute_read_query(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return result
#     except (OperationalError, ProgrammingError) as e:
#         print(f'''The error '{e}' occurred''')
#
#
# def get_users_posts(connection):
#     select_users_posts = '''
#         SELECT
#           users.id,
#           users.name,
#           posts.description
#         FROM
#           posts
#           INNER JOIN users ON users.id = posts.user_id
#     '''
#
#     users_posts = execute_read_query(connection, select_users_posts)
#
#     for users_post in users_posts:
#         print(users_post)
#
#
# def users_posts_comments_query():
#     return '''
#         SELECT
#           posts.description as post,
#           text as comment,
#           name
#         FROM
#           posts
#           INNER JOIN comments ON posts.id = comments.post_id
#           INNER JOIN users ON users.id = comments.user_id
#     '''
#
#
# def get_users_posts_comments(connection, query):
#     posts_comments_users = execute_read_query(connection, query)
#
#     for posts_comments_user in posts_comments_users:
#         print(posts_comments_user)
#
#
# def get_column_names(connection, query):
#     cursor = connection.cursor()
#     cursor.execute(query)
#     cursor.fetchall()
#
#     column_names = [description[0] for description in cursor.description]
#     print(column_names)
#
#
# def get_post_likes(connection):
#     select_post_likes = '''
#         SELECT
#           p.description as post,
#           COUNT(l.id) as likes
#         FROM
#           likes l,
#           posts p
#         WHERE
#           p.id = l.post_id
#         GROUP BY
#           l.post_id, p.description
#     '''
#
#     post_likes = execute_read_query(connection, select_post_likes)
#
#     for post_like in post_likes:
#         print(post_like)
#
#
# def select_posts(connection):
#     select_post_description = 'SELECT description FROM posts WHERE id = 2'
#
#     post_description = execute_read_query(connection, select_post_description)
#
#     for description in post_description:
#         print(description)
#
#
# def update_posts(connection):
#     update_post_description = '''
#         UPDATE
#           posts
#         SET
#           description = 'The weather has become pleasant now'
#         WHERE
#           id = 2
#     '''
#
#     execute_query(connection, update_post_description, False)


def main():
    connection = create_connection(
        # db_name='sm_app',
        db_name=environ['POSTGRES_DB'],
        db_user=environ['POSTGRES_USER'],
        db_password=environ['POSTGRES_PASSWORD'],
    )

    # create_database_query = 'CREATE DATABASE sm_app'
    # create_database(connection, create_database_query)

    # create_tables(connection)

    # insert_users(connection)
    # insert_posts(connection)
    # insert_comments_and_likes(connection)

    # select_users = 'SELECT * FROM users'
    # users = execute_read_query(connection, select_users)
    # for user in users:
    #     print(user)

    # select_posts = 'SELECT * FROM posts'
    # posts = execute_read_query(connection, select_posts)
    # for post in posts:
    #     print(post)

    # get_users_posts(connection)

    # get_users_posts_comments(connection, users_posts_comments_query())

    # get_column_names(connection, users_posts_comments_query())

    # get_post_likes(connection)

    # select_posts(connection)
    # update_posts(connection)
    # select_posts(connection)

    # delete_comment = 'DELETE FROM comments WHERE id = 5'
    # execute_query(connection, delete_comment)


if __name__ == '__main__':
    main()
