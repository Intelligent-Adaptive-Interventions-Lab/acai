DROP TABLE IF EXISTS chats
DROP TABLE IF EXISTS quiz

CREATE TABLE chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT NOT NULL,
    chat_log TEXT NOT NULL
);

CREATE TABLE quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quiz_id TEXT NOT NULL,
    receiver TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    reward TEXT NOT NULL,
    answer TEXT NOT NULL,
    actual_reward TEXT NOT NULL,
    time1 TEXT NOT NULL,
    time2 TEXT NOT NULL
);

