# python imports
import flask
import uuid

# project imports
import modules.database

# init application and setup for development
app = flask.Flask(__name__)
app.secret_key = 'EinsteinFlyingPigsMashup'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# init database - only done once,single instance used later everywhere
db = modules.database.database()


@app.route('/')
def get_home():
    return flask.render_template(
        'home.html',
        username=flask.session.get('username')
    )


@app.route('/browse/')
def get_browse():
    imglist = [{
        'uuid': uuid.uuid4(),
        'author': 'Kalle',
        'time': '2017-10-26',
        'title': 'Jotakin muuta!'
    } for i in range(0, 20)]
    return flask.render_template(
        'browse.html',
        imagelist=imglist,
        username=flask.session.get('username')
    )


@app.route('/statistics/', methods=['GET'])
def get_statistics():
    return flask.render_template(
        'statistics.html',
        username=flask.session.get('username')
    )


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
    imagedata = db.get_image_data(imdig)
    return flask.render_template(
        'image.html',
        imagetitle='Norppa?!?!?',
        imageid=imgid,
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
    return flask.redirect('/image/{}/'.format(imageid))


@app.route('/action/upload/', methods=['POST'])
def post_upload():
    return flask.redirect('/image/{}/'.format(uuid.uuid4()))


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
