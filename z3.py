from flask import Flask, request, session, flash
from src import ResourceManager, DatabaseManager, ResponseManager, UserFileManager

__page_login = "login.html"
__page_register = "register.html"
__page_list = "list.html"
__page_add_file = "add_file.html"

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4uygkuhjv[$:VHW]'
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    # SESSION_COOKIE_SECURE=True
)


@app.route('/cholewp1/z3/')
def index():
    if 'username' in session:
        return ResourceManager.send_html(__page_list)
    return ResourceManager.send_html(__page_login)


@app.route('/cholewp1/z3/login')
def send_html_login():
    return index()


@app.route('/cholewp1/z3/register')
def send_html_register():
    # return ResponseManager.create_response_403()
    return ResourceManager.send_html(__page_register)


@app.route('/cholewp1/z3/list')
def send_html_list():
    return ResourceManager.send_html(__page_list)


@app.route('/cholewp1/z3/add_file')
def send_html_add_file():
    return ResourceManager.send_html(__page_add_file)


@app.route('/cholewp1/z3/template/<path:path>')
def send_html_template(path):
    return ResourceManager.send_html_template(path)


@app.route('/cholewp1/z3/css/<path:path>')
def send_css(path):
    return ResourceManager.send_css(path)


@app.route('/cholewp1/z3/js/<path:path>')
def send_js(path):
    return ResourceManager.send_js(path)


@app.route('/cholewp1/z3/img/<path:path>')
def send_img(path):
    return ResourceManager.send_img(path)


@app.route('/cholewp1/z3/ws/login/', methods=['POST'])
def login():
    username = request.form['user-id']
    if DatabaseManager.authenticate_user(username, request.form['password']):
        session['username'] = username
        return ResourceManager.send_html(__page_list)
    else:
        ResponseManager.create_response_401()


@app.route('/cholewp1/z3/ws/logout/', methods=['POST'])
def logout():
    session.pop('username', None)
    return ResourceManager.send_html(__page_login)


@app.route('/cholewp1/z3/ws/register/', methods=['POST'])
def register():
    new_user = DatabaseManager.add_new_user(request.form['user-id'], request.form['password'])
    if new_user is not None:
        return ResourceManager.send_html(__page_login)
    else:
        return ResponseManager.create_response_401()


@app.route('/cholewp1/z3/ws/files/list/', methods=['GET'])
def get_file_list():
    if 'username' not in session:
        return ResponseManager.create_response_401()

    return ResponseManager.create_response_200(
        UserFileManager.get_user_file_names(session['username']),
        "application/json")


@app.route('/cholewp1/z3/ws/files/add/', methods=['POST'])
def post_file():
    if 'username' not in session:
        return ResponseManager.create_response_401()

    if 'file' not in request.files:
        flash("No file part!")
        return ResponseManager.create_response_400()

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return ResponseManager.create_response_400()

    if UserFileManager.save_user_file(
        session['username'],
        file):
        return ResponseManager.create_response_200(None, None)
    else:
        return ResponseManager.create_response_403()


@app.route('/cholewp1/z3/ws/files/get/<path:path>', methods=['GET'])
def get_file(path):
    if 'username' not in session:
        return ResponseManager.create_response_401()

    return ResponseManager.create_response_200(
        UserFileManager.get_user_file(session['username'], path),
        'application/octet-stream'
    )
