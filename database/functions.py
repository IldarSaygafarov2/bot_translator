import psycopg2
from config.loader import app_config


def connect():
    connection = psycopg2.connect(
        host=app_config.db.host,
        user=app_config.db.user,
        database=app_config.db.database,
        password=app_config.db.password,
        port=app_config.db.port
    )
    cursor = connection.cursor()
    return connection, cursor


def create_users_table():
    connection, cursor = connect()
    sql = '''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        chat_id BIGINT UNIQUE
    );
    '''
    cursor.execute(sql)
    connection.commit()
    cursor.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS username TEXT')
    connection.commit()
    print('users table created')


def create_translations_table():
    connection, cursor = connect()
    sql = """
        CREATE TABLE IF NOT EXISTS translations(
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            lang_from VARCHAR(5),
            lang_to VARCHAR(5),
            original TEXT,
            translated TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """
    cursor.execute(sql)
    connection.commit()
    print('translations table created')


def add_user(chat_id, username):
    connection, cursor = connect()

    sql = """
        INSERT INTO users(chat_id, username)
        VALUES (%s, %s)
        ON CONFLICT (chat_id)
        DO UPDATE SET username = %s;
    """
    cursor.execute(sql, (chat_id,username, username))
    connection.commit()
    print(f'user with {chat_id=} added')


def get_user_id(chat_id):
    connection, cursor = connect()
    sql = "SELECT id FROM users WHERE chat_id = %s;"
    # (id,)|None
    cursor.execute(sql, (chat_id,))
    result = cursor.fetchone()
    if result is None:
        return None

    return result[0]


def get_user_translations(chat_id):
    connection, cursor = connect()

    user_id = get_user_id(chat_id)
    if user_id is None:
        return []

    sql = 'SELECT * FROM translations WHERE user_id = %s;'
    cursor.execute(sql, (user_id,))
    result = cursor.fetchall()
    return result



def add_translation(lang_from, lang_to, original, translated, chat_id):
    connection, cursor = connect()
    user_id = get_user_id(chat_id)
    if user_id is None:
        return

    sql = '''
    INSERT INTO translations(lang_from, lang_to, original, translated, user_id)
    VALUES (%s,%s,%s,%s,%s);
    '''
    cursor.execute(sql, (lang_from, lang_to, original, translated, user_id))
    connection.commit()
    print(f'translation for user with {chat_id=} added')


def delete_translation(translation_id):
    connection, cursor = connect()

    sql = 'DELETE FROM translations WHERE id = %s;'
    cursor.execute(sql, (translation_id,))
    connection.commit()
    print(f'translation with {translation_id=} deleted')


def get_all_users():
    connection, cursor = connect()
    sql = 'SELECT chat_id, username FROM users;'
    cursor.execute(sql)
    users = cursor.fetchall()
    return users


def get_user_chat_id(user_id):
    connection, cursor = connect()
    sql = 'SELECT chat_id FROM users WHERE id = %s;'
    cursor.execute(sql, (user_id,))
    chat_id = cursor.fetchone()
    if chat_id is None:
        return None
    return chat_id[0]