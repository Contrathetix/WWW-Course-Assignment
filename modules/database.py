# python imports
import os
import uuid
import sqlite3

# passlib from PyPi
from passlib.hash import pbkdf2_sha256


class database(object):

    dbpath = os.path.abspath('./data/database.db')
    sqlpath = os.path.abspath('./data/database.sql')

    def __init__(self):
        super().__init__()
        # remove potential old database file at launch
        if os.path.isfile(self.dbpath):
            os.unlink(self.dbpath)
        # cleanup uploaded files storage, as well
        uploadpath = os.path.join(os.path.abspath('.'), 'static', 'uploads')
        for fp in os.scandir(uploadpath):
            os.unlink(fp.path)
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
            pwhash = pbkdf2_sha256.hash(password[0])
            self.cursor.execute(
                'INSERT INTO users(username,pwhash,usergroup) ' +
                'VALUES ( (?), (?), (SELECT id FROM usergroups WHERE groupname="registered") )',
                (username, pwhash)
            )
            return 'Account creation successful!'
        except Exception as exc:
            print(exc)
        return 'Account creation failed.'

    def upload_image(self, username, imagetitle, imagefile):
        try:
            imageid = str(uuid.uuid4())
            outputpath = os.path.join(
                os.path.abspath('.'), 'static', 'uploads', imageid + '.jpg'
            )
            imagefile.save(outputpath)
            self.cursor.execute(
                'INSERT INTO images(uuid,title,uploader) ' +
                'VALUES ( (?), (?), (SELECT id FROM users WHERE username=?))',
                (imageid, imagetitle, username)
            )
            return imageid
        except Exception as exc:
            print(exc)
        return None

    def check_credentials(self, username, password):
        try:
            if (username == 'guest'):
                return True
            self.cursor.execute(
                'SELECT pwhash FROM users WHERE username=?',
                (username,)
            )
            pwhash = self.cursor.fetchone()['pwhash']
            if (pwhash):
                return pbkdf2_sha256.verify(password, pwhash)
        except Exception as exc:
            print(exc)
        return False

    def get_image_data_complete(self):
        try:
            self.cursor.execute(
                'SELECT ' +
                'images.uuid AS uuid, ' +
                'images.title AS title, ' +
                'users.username AS uploader ' +
                'FROM images INNER JOIN users ' +
                'ON users.id=images.uploader'
            )
            return self.cursor.fetchall()
        except Exception as exc:
            print(exc)
        return []

    def get_image_data(self, imageid=None):
        try:
            self.cursor.execute(
                'SELECT ' +
                'images.uuid AS uuid, ' +
                'images.title AS title, ' +
                'users.username AS uploader ' +
                'FROM images INNER JOIN users ' +
                'ON users.id=images.uploader ' +
                'WHERE images.uuid=?',
                (str(imageid),)
            )
            return self.cursor.fetchone()
        except Exception as exc:
            print(exc)
        return None
