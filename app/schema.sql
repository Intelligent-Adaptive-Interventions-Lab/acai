DROP TABLE IF EXISTS chats
DROP TABLE IF EXISTS interfaceSession
DROP TABLE IF EXISTS linkClick

CREATE TABLE chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT NOT NULL,
    chat_log TEXT NOT NULL
);

CREATE TABLE linkClick (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interfaceSession (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    pre_mindful TEXT,
    pre_stress TEXT,
    pre_aware TEXT,
    pre_perspective TEXT,
    diary_1 TEXT,
    diary_2 TEXT,
    post_mindful TEXT,
    post_stress TEXT,
    post_aware TEXT,
    session_start_ts TIMESTAMP,
    video_name TEXT,
    pre_survey_click_ts TIMESTAMP,
    main_interface_click_ts_1 TIMESTAMP,
    main_interface_click_ts_2 TIMESTAMP,
    reflect_chatlog TEXT,
    post_survey_click_ts TIMESTAMP
);
