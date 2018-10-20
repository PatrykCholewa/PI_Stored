from html import escape

from flask import Flask, request, session
from src import ResourceManager, DatabaseManager, ResponseManager

__page_login = "login.html"
__page_register = "register.html"

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4uygkuhjv[$:VHW]'


@app.route('/cholewp1/z3/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return ResourceManager.send_html(__page_login)


@app.route('/cholewp1/z3/register/')
def send_html_register():
    return ResourceManager.send_html(__page_register)


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
        return ResponseManager.create_response_200("OK", "text/plain")
    #     app.logger.info('%s logged in successfully', user.username)
    #     return redirect(url_for('index'))
    else:
        ResponseManager.create_response_401()


@app.route('/cholewp1/z3/ws/logout/', methods=['POST'])
def logout():
    session.pop('username', None)
    return ResourceManager.send_html(__page_login)


@app.route('/cholewp1/z3/ws/register/', methods=['POST'])
def register():
    # @TODO
    return
