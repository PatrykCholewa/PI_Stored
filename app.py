from flask import Flask, request, session
from src import ResourceManager, DatabaseManager, ResponseManager

__page_login = "login.html"
__page_register = "register.html"
__page_list = "list.html"
__page_add_file = "add_file.html"

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4uygkuhjv[$:VHW]'


@app.route('/cholewp1/z3/')
def index():
    if 'username' in session:
        return ResourceManager.send_html(__page_list)
    return ResourceManager.send_html(__page_login)


@app.route('/cholewp1/z3/register')
def send_html_register():
    return ResourceManager.send_html(__page_register)


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
    user = DatabaseManager.get_user_by_username(request.form['user-id'])
    if user.check_password(request.form['password']):
        session['username'] = user.username
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
        # @TODO better response
        return ResponseManager.create_response_404()


@app.route('/cholewp1/z3/ws/files/add/', methods=['POST'])
def post_file():
    # @TODO
    return


@app.route('/cholewp1/z3/ws/files/list/', methods=['GET'])
def get_file_list():
    # @TODO
    return


@app.route('/cholewp1/z3/ws/files/get', methods=['GET'])
def get_file():
    # @TODO
    return
