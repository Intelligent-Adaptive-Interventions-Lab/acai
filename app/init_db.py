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

cur.execute("INSERT INTO quiz (quiz_id, recevier, difficulty, reward, answer, actual_reward, time1, time2) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('127.0.0.1', '1', '1', '1', '1', '1', '1', '1')
            )

connection.commit()
connection.close()
