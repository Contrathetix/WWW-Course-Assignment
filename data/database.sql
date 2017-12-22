CREATE TABLE usergroups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    groupname TEXT UNIQUE NOT NULL,
    isadmin BOOLEAN DEFAULT 0
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    usergroup INTEGER NOT NULL,
    pwhash TEXT NOT NULL,

    FOREIGN KEY (usergroup) REFERENCES usergroups(id) ON DELETE CASCADE
);

CREATE TABLE images (
    uuid TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    uploader INTEGER NOT NULL,

    FOREIGN KEY (uploader) REFERENCES users(id) ON DELETE CASCADE
) WITHOUT ROWID;

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT NOT NULL,
    uploader INTEGER NOT NULL,
    imageid TEXT NOT NULL,

    FOREIGN KEY (uploader) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (imageid) REFERENCES images(uuid) ON DELETE CASCADE
);

INSERT INTO usergroups(groupname,isadmin) VALUES ('admins',1);
INSERT INTO usergroups(groupname,isadmin) VALUES ('registered',0);
INSERT INTO usergroups(groupname,isadmin) VALUES ('guests',0);

INSERT INTO users(username,usergroup,pwhash) VALUES (
    ('guest'),
    (SELECT id FROM usergroups WHERE groupname='guests'),
    'notanactualpwhash'
);
