# python imports
import flask
import uuid

# project imports
import modules.database

# init application
app = flask.Flask(__name__)

# not secure, but will do for now
app.secret_key = str(uuid.uuid4())

# instruct jinja to clean-up blocks and to auto-reload altered templates
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# init database - only done once per app
db = modules.database.database()


@app.route('/')
def get_home():
    # render homepage / landing page
    return flask.render_template(
        'home.html',
        username=flask.session.get('username')
    )


@app.route('/browse/')
def get_browse():
    # print out a list of all images ever saved in the system,
    # obviously not practical in the long term but will do for now
    return flask.render_template(
        'browse.html',
        imagelist=db.get_image_data_complete(),
        username=flask.session.get('username')
    )


# @app.route('/statistics/', methods=['GET'])
# def get_statistics():
#    return flask.render_template(
#        'statistics.html',
#        username=flask.session.get('username')
#    )


@app.route('/upload/', methods=['GET'])
def get_upload():
    return flask.render_template(
        'upload.html',
        username=flask.session.get('username')
    )


@app.route('/register/', methods=['GET'])
def get_register():
    return flask.render_template(
        'register.html',
        username=flask.session.get('username')
    )


@app.route('/login/', methods=['GET'])
def get_login():
    return flask.render_template(
        'login.html',
        username=flask.session.get('username')
    )


@app.route('/logout/', methods=['GET'])
def get_logout():
    flask.session['username'] = None
    return flask.redirect('/')


@app.route('/image/<uuid:imgid>/')
def get_image(imgid=None):
    imagedata = db.get_image_data(str(imgid))
    return flask.render_template(
        'image.html',
        imagedata=imagedata,
        username=flask.session.get('username')
    )


@app.route('/action/login/', methods=['POST'])
def post_login():
    loginsuccess = db.check_credentials(
        flask.request.form.get('username'),
        flask.request.form.get('password')
    )
    if (loginsuccess):
        flask.session['username'] = flask.request.form.get('username')
        return flask.redirect('/browse/')
    else:
        flask.flash('Login failed, please check your credentials.')
        return flask.redirect('/login/')


@app.route('/action/register/', methods=['POST'])
def post_register():
    message = db.register_user(
        username=flask.request.form['username'],
        password=(
            flask.request.form['password1'],
            flask.request.form['password2']
        )
    )
    flask.flash(message)
    return flask.redirect('/register/')


@app.route('/action/comment/<uuid:imageid>/', methods=['POST'])
def post_comment(imageid=None):
    try:
        inputdata = flask.request.get_json(force=True)
        # print(inputdata)
        output = db.upload_comment(
            imageid=str(imageid),
            username=flask.session.get('username'),
            comment=inputdata['comment']
        )
        # print(output)
        return flask.jsonify(output)
    except Exception as exc:
        return 500


@app.route('/action/get-comments/<uuid:imageid>/', methods=['GET'])
def get_comments_for_image(imageid=None):
    return flask.jsonify(db.get_comments(imageid=str(imageid)))


@app.route('/action/upload/', methods=['POST'])
def post_upload():
    imageid = db.upload_image(
        username=flask.session.get('username'),
        imagetitle=flask.request.form['title'],
        imagefile=flask.request.files['file']
    )
    if (imageid):
        flask.flash('Upload success!')
        return flask.redirect('/image/{}/'.format(imageid))
    else:
        flask.flash('Upload failed, an error occurred...')
        return flask.redirect('/upload/')


@app.route('/api/browse/')
def api_browse():
    # return flask.jsonify([
    #    {'filename': 'random.jpg', 'title': 'Random', 'uuid': uuid.uuid4()}
    # ])
    return 404


if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=8080, debug=False)
    except KeyboardInterrupt:
        print('Terminated by user keypress')
    except Exception as exc:
        print(exc)
    db.close()
