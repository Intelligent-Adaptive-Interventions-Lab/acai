import sqlite3

# Connect to SQLite database
connection = sqlite3.connect('database.db')

# Execute the schema script to create tables
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insert sample data into the 'chats' table
cur.execute("INSERT INTO chats (user_id, chat_log) VALUES (?, ?)",
            ('127.0.0.1', 'Content for the first chat'))

cur.execute("INSERT INTO chats (user_id, chat_log) VALUES (?, ?)",
            ('127.0.0.1', 'Content for the second chat'))

# Insert sample data into the 'linkClick' table
cur.execute("INSERT INTO linkClick (user_id) VALUES (?)",
            ('127.0.0.1',))

# Insert sample data into the 'interfaceSession' table
cur.execute("""
    INSERT INTO interfaceSession (
        user_id, pre_mindful, pre_stress, pre_aware, pre_perspective, 
        diary_1, diary_2, post_mindful, post_stress, post_aware, 
        session_start_ts, video_name, pre_survey_click_ts, main_interface_click_ts_1, 
        main_interface_click_ts_2, reflect_chatlog, post_survey_click_ts
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ('127.0.0.1', 'Pre-Mindful Response', 'Pre-Stress Response', 'Pre-Aware Response', 
      'Pre-Perspective Response', 'Diary Entry 1', 'Diary Entry 2', 
      'Post-Mindful Response', 'Post-Stress Response', 'Post-Aware Response',
      '2023-01-01 00:00:00', 'Sample Video', '2023-01-01 00:00:00', 
      '2023-01-01 00:00:00', '2023-01-01 00:00:00', 'Reflect Chatlog', '2023-01-01 00:00:00'))

# Commit the changes and close the connection
connection.commit()
connection.close()
