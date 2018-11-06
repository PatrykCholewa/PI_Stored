from flask import Flask, request, session
from src import ResourceManager, DatabaseManager, ResponseManager, CookieManager

__page_login = "login.html"
__page_register = "register.html"
__page_list = "list.html"
__page_add_file = "add_file.html"

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4uygkuhjv[$:VHW]'
app.config["APPLICATION_ROOT"] = "/cholewp1/webapp/"
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    # SESSION_COOKIE_SECURE=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    # REMEMBER_COOKIE_SECURE=True
)


def is_not_logged():
    if 'sid' not in session:
        return True

    return not DatabaseManager.check_session_valid(session['username'], session['sid'])


@app.route('/cholewp1/webapp/')
def index():
    if is_not_logged():
        return ResourceManager.send_html(__page_login)

    return ResourceManager.send_html(__page_list)


@app.route('/cholewp1/webapp/login')
def send_html_login():
    return index()


@app.route('/cholewp1/webapp/register')
def send_html_register():
    return ResponseManager.create_response_403()
    # return ResourceManager.send_html(__page_register)


@app.route('/cholewp1/webapp/list')
def send_html_list():
    if is_not_logged():
        return ResponseManager.create_response_401()

    return ResourceManager.send_html(__page_list)


@app.route('/cholewp1/webapp/add_file')
def send_html_add_file():
    if is_not_logged():
        return ResponseManager.create_response_401()

    return ResourceManager.send_html(__page_add_file)


@app.route('/cholewp1/webapp/template/<path:path>')
def send_html_template(path):
    return ResourceManager.send_html_template(path)


@app.route('/cholewp1/webapp/css/<path:path>')
def send_css(path):
    return ResourceManager.send_css(path)


@app.route('/cholewp1/webapp/js/<path:path>')
def send_js(path):
    return ResourceManager.send_js(path)


@app.route('/cholewp1/webapp/img/<path:path>')
def send_img(path):
    return ResourceManager.send_img(path)


@app.route('/cholewp1/webapp/cookie/user/')
def get_new_user_cookie():
    if is_not_logged():
        return ResponseManager.create_response_401()

    response = ResponseManager.create_response_200("", "text,plain")
    response = CookieManager.set_user_cookie_to_response(response, session['username'])
    return response


@app.route('/cholewp1/webapp/ws/login/', methods=['POST'])
def login():
    username = request.form['user-id']
    if DatabaseManager.authenticate_user(username, request.form['password']):
        sid = DatabaseManager.create_new_session(username)
        session['username'] = username
        session['sid'] = sid

        response = ResourceManager.send_html(__page_list)
        response = CookieManager.set_user_cookie_to_response(response, session['username'])
        return response
    else:
        ResponseManager.create_response_401()


@app.route('/cholewp1/webapp/ws/logout/', methods=['POST'])
def logout():
    if is_not_logged():
        return ResponseManager.create_response_401()

    DatabaseManager.delete_session(session['username'])
    session.pop('sid', None)
    session.pop('username', None)
    return ResourceManager.send_html(__page_login)


@app.route('/cholewp1/webapp/ws/register/', methods=['POST'])
def register():
    return ResponseManager.create_response_403()
    # new_user = DatabaseManager.add_new_user(request.form['user-id'], request.form['password'])
    # if new_user is not None:
    #     return ResourceManager.send_html(__page_login)
    # else:
    #     return ResponseManager.create_response_401()
