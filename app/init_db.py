import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO chats (user_id, chat_log) VALUES (?, ?)",
            ('127.0.0.1', 'Content for the first chat')
            )

cur.execute("INSERT INTO chats (user_id, chat_log) VALUES (?, ?)",
            ('127.0.0.1', 'Content for the second chat')
            )

connection.commit()
connection.close()
