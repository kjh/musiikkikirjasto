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

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    collection_id INTEGER REFERENCES collections,
    UNIQUE (user_id, collection_id)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE collection_tags (
    collection_id INTEGER REFERENCES collections,
    tag_id INTEGER REFERENCES tags,
    PRIMARY KEY (collection_id, tag_id)
);