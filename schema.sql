CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE collections (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE releases (
    id INTEGER PRIMARY KEY,
    artist TEXT,
    title TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    collection_id INTEGER REFERENCES collections
);
