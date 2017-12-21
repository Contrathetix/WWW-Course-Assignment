CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isadmin BOOLEAN DEFAULT 0,
    username TEXT UNIQUE NOT NULL,
    pwd TEXT NOT NULL
);

CREATE TABLE images (
    uuid TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    uploader INTEGER NOT NULL,

    FOREIGN KEY (uploader) REFERENCES users(id) ON DELETE CASCADE
) WITHOUT ROWID;

INSERT INTO users(isadmin,username,pwd) VALUES (1,'admin','salasana');
