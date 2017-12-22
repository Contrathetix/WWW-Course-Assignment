# python imports
import os
import uuid
import sqlite3

# passlib from PyPi
from passlib.hash import pbkdf2_sha256


class database(object):

    # relative paths for database file and the sql file
    dbpath = os.path.abspath('./data/database.db')
    sqlpath = os.path.abspath('./data/database.sql')

    def __init__(self):
        super().__init__()
        # remove potential old database file at launch
        if os.path.isfile(self.dbpath):
            os.unlink(self.dbpath)
        # cleanup uploaded files storage, as well
        uploadpath = os.path.join(os.path.abspath('.'), 'static', 'uploads')
        try:
            if (os.path.isdir(uploadpath) is False):
                os.makedirs(uploadpath)
            for fp in os.scandir(uploadpath):
                os.unlink(fp.path)
        except Exception as exc:
            print(exc)
        # connect to database and prepare it
        self.db = sqlite3.connect(self.dbpath)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        # read the sql file into the database
        with open(self.sqlpath, 'r') as sql:
            self.cursor.executescript(sql.read())

    def close(self):
        # close the database and cursor
        try:
            self.cursor.close()
            self.db.close()
        except Exception as exc:
            print(exc)

    def register_user(self, username, password):
        # add user to the system, assuming username and pwd were provided,
        # returns a message to be displayed to the user
        try:
            if (password[0] != password[1]):
                return 'Passwords do not match!'
            if (len(username) < 1 or len(password[0]) < 1):
                return 'Please supply long enough password and username.'
            # hashing with passlib, as I understand it, salt is generated
            # automatically by passlib and included in the hash
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
        # upload an image file, generate a new uuid for it and save the file,
        # and also make a record in the database for the image
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

    def upload_comment(self, imageid, username, comment):
        # add a comment to the database, by a user, for an image
        # print('{} commented on {}: {}'.format(username, imageid, comment))
        try:
            self.cursor.execute(
                'INSERT INTO comments(comment,uploader,imageid) ' +
                'VALUES ( ' +
                '(?), ' +
                '(SELECT id FROM users WHERE username=?), ' +
                '(SELECT uuid FROM images WHERE uuid=?) )',
                (comment, username, imageid)
            )
            return True
        except Exception as exc:
            print(exc)
        return False

    def check_credentials(self, username, password):
        # verify credentials provided by a user, return True or False
        # depending on whether such a user exists with such a password
        try:
            if (username == 'guest'):
                return True
            self.cursor.execute(
                'SELECT pwhash FROM users WHERE username=?',
                (username,)
            )
            pwhash = self.cursor.fetchone()['pwhash']
            if (pwhash):
                # using the password hash verification from passlib
                return pbkdf2_sha256.verify(password, pwhash)
        except Exception as exc:
            print(exc)
        return False

    def get_image_data_complete(self):
        # get data for all images stored in the database
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

    def get_comments(self, imageid=None):
        # fetch comments for a specific image
        try:
            self.cursor.execute(
                'SELECT ' +
                'comments.comment AS comment, ' +
                'users.username AS username ' +
                'FROM comments INNER JOIN users ' +
                'ON comments.uploader=users.id ' +
                'WHERE comments.imageid=?',
                (imageid,)
            )
            return [{
                'comment': dbrow['comment'],
                'username': dbrow['username']
            } for dbrow in self.cursor.fetchall()]
        except Exception as exc:
            print(exc)
        return None

    def get_image_data(self, imageid=None):
        # return imagedata for a single image
        try:
            self.cursor.execute(
                'SELECT ' +
                'images.uuid AS uuid, ' +
                'images.title AS title, ' +
                'users.username AS uploader ' +
                'FROM images INNER JOIN users ' +
                'ON users.id=images.uploader ' +
                'WHERE images.uuid=?',
                (imageid,)
            )
            return self.cursor.fetchone()
        except Exception as exc:
            print(exc)
        return None
