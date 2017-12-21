import os
import sqlite3


class database(object):

    dbpath = os.path.abspath('./data/database.db')
    sqlpath = os.path.abspath('./data/database.sql')

    def __init__(self):
        super().__init__()
        if os.path.isfile(self.dbpath):
            os.unlink(self.dbpath)
        self.db = sqlite3.connect(self.dbpath)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        with open(self.sqlpath, 'r') as sql:
            self.cursor.executescript(sql.read())

    def close(self):
        try:
            self.cursor.close()
            self.db.close()
        except Exception as exc:
            print(exc)

    def register_user(self, username, password):
        try:
            if (password[0] != password[1]):
                return 'Passwords do not match!'
            if (len(username) < 1 or len(password[0]) < 1):
                return 'Please supply long enough password and username.'
            self.cursor.execute(
                'INSERT INTO users(username,pwd) VALUES (?,?)',
                (username, password[0])
            )
            return 'Account creation successful!'
        except Exception as exc:
            return 'Account creation failed.'

    def check_credentials(self, username, password):
        try:
            self.cursor.execute(
                'SELECT COUNT (*) AS matches FROM users WHERE username=? AND pwd=?',
                (username, password)
            )
            if (self.cursor.fetchone()['matches'] > 0):
                return username
        except Exception as exc:
            print(exc)
        return None
