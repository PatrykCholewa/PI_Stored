from flask import Flask, request
from src import ResourceManager

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4v[$:VHW]'


@app.route('/cholewp1/z3/')
def index():
    return ResourceManager.send_html("login.html")


@app.route('/cholewp1/z3/register/')
def send_html_register():
    return ResourceManager.send_html("register.html")


@app.route('/cholewp1/z3/css/<path:path>')
def send_css(path):
    return ResourceManager.send_css(path)


@app.route('/cholewp1/z3/js/<path:path>')
def send_js(path):
    return ResourceManager.send_js(path)


@app.route('/cholewp1/z3/img/<path:path>')
def send_img(path):
    return ResourceManager.send_img(path)


@app.route('/cholewp1/z3/ws/login', methods=['POST'])
def login():
    # user = get_user(request.form['username'])
    # if user.check_password(request.form['password']):
    #     login_user(user)
    #     app.logger.info('%s logged in successfully', user.username)
    #     return redirect(url_for('index'))
    # else:
    #     app.logger.info('%s failed to log in', user.username)
    #     abort(401)
    return


@app.route('/cholewp1/z3/ws/register/')
def register():
    # @TODO
    return
