import sqlite3

# SQLITE_DB_PATH = '/var/www/html/acaidb/database.db'
SQLITE_DB_PATH = './database.db'

def add_new_chat_log(user_id, chat_log):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO chats
                                (user_id, chat_log) 
                                VALUES 
                                (?,?);"""
        param_tuple = (user_id, chat_log)
        count = cursor.execute(sqlite_insert_query, param_tuple)
        sqliteConnection.commit()
        print(
            "Record inserted successfully into SqliteDb_developers table ",
            cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def track_link_click(user_id, timestamp):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO linkClick
                                (user_id, timestamp) 
                                VALUES 
                                (?,?);"""
        param_tuple = (user_id, timestamp)
        count = cursor.execute(sqlite_insert_query, param_tuple)
        sqliteConnection.commit()
        print(
            "Record inserted successfully into SqliteDb_developers table ",
            cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def add_new_user_to_diary_study(user_id, session_start_ts):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO interfaceSession (
                                user_id, session_start_ts
                                ) VALUES (?, ?);"""
        param_tuple = (user_id, session_start_ts)
        count = cursor.execute(sqlite_insert_query, param_tuple)
        sqliteConnection.commit()
        print(
            "Record inserted successfully into SqliteDb_developers table ",
            cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def get_last_id_from_user_id(user_id):
    sqliteConnection = None
    last_id = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        query_sql = "SELECT MAX(id) FROM interfaceSession WHERE user_id = ?;"

        param_tuple = (user_id)
        count = cursor.execute(query_sql, param_tuple)

        last_id = cursor.fetchone()[0]

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    
    print(f'found last id: {last_id}')

    return last_id

def update_pre_survey(user_id, pre_mindful, pre_stress, pre_aware, pre_perspective, pre_survey_click_ts):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """UPDATE interfaceSession
                                SET pre_mindful = ?, 
                                pre_stress = ?,
                                pre_aware = ?,
                                pre_perspective = ?,
                                pre_survey_click_ts = ?
                                WHERE id = (
                                    SELECT MAX(id)
                                    FROM interfaceSession
                                    WHERE user_id = ?
                                );"""
        param_tuple = (pre_mindful, pre_stress, pre_aware, pre_perspective, pre_survey_click_ts, user_id)
        count = cursor.execute(sqlite_insert_query, param_tuple)
        sqliteConnection.commit()
        print(
            "Record inserted successfully into SqliteDb_developers table ",
            cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def udpate_diary(user_id, diary_1, diary_2, video_name, main_interface_click_ts_1):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """UPDATE interfaceSession
                                SET diary_1 = ?, 
                                diary_2 = ?,
                                video_name = ?,
                                main_interface_click_ts_1 = ?
                                WHERE id = (
                                    SELECT MAX(id)
                                    FROM interfaceSession
                                    WHERE user_id = ?
                                );"""
        param_tuple = (diary_1, diary_2, video_name, main_interface_click_ts_1, user_id)
        count = cursor.execute(sqlite_insert_query, param_tuple)
        sqliteConnection.commit()
        print(
            "Record inserted successfully into SqliteDb_developers table ",
            cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def update_reflect_chat(user_id, reflect_chatlog):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """UPDATE interfaceSession
                                SET reflect_chatlog = ?
                                WHERE id = (
                                    SELECT MAX(id)
                                    FROM interfaceSession
                                    WHERE user_id = ?
                                );"""
        param_tuple = (reflect_chatlog, user_id)
        count = cursor.execute(sqlite_insert_query, param_tuple)
        sqliteConnection.commit()
        print(
            "Record inserted successfully into SqliteDb_developers table ",
            cursor.rowcount)
        cursor.close()
        
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def update_reflect(user_id, diary_1, diary_2, main_interface_click_ts_2):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """UPDATE interfaceSession
                                SET diary_1 = ?, 
                                diary_2 = ?,
                                main_interface_click_ts_2 = ?
                                WHERE id = (
                                    SELECT MAX(id)
                                    FROM interfaceSession
                                    WHERE user_id = ?
                                );"""
        param_tuple = (diary_1, diary_2, main_interface_click_ts_2, user_id)
        count = cursor.execute(sqlite_insert_query, param_tuple)
        sqliteConnection.commit()
        print(
            "Record inserted successfully into SqliteDb_developers table ",
            cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def update_post_survey(user_id, post_mindful, post_stress, post_aware, post_survey_click_ts):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """UPDATE interfaceSession
                                SET post_mindful = ?, 
                                post_stress = ?,
                                post_aware = ?,
                                post_survey_click_ts = ?
                                WHERE id = (
                                    SELECT MAX(id)
                                    FROM interfaceSession
                                    WHERE user_id = ?
                                );"""
        param_tuple = (post_mindful, post_stress, post_aware, post_survey_click_ts, user_id)
        count = cursor.execute(sqlite_insert_query, param_tuple)
        sqliteConnection.commit()
        print(
            "Record inserted successfully into SqliteDb_developers table ",
            cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def get_diary_answers_from_latest_user_id(user_id):
    sqliteConnection = None
    diary_1, diary_2 = None, None
    try:
        sqliteConnection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        query_sql = """SELECT diary_1, diary_2
                        FROM interfaceSession 
                        WHERE id = (
                            SELECT MAX(id)
                            FROM interfaceSession
                            WHERE user_id = ?
                        );"""
        param_tuple = (user_id)
        count = cursor.execute(query_sql, param_tuple)

        diary_1, diary_2 = cursor.fetchone()

        print(f'diary_answers: {diary_1}, {diary_2}')
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to select data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return diary_1, diary_2
