from flask import Flask, request
import src.ResponseManager as sResponseManager

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4v[$:VHW]'


def send_from_directory(path, content_type):
    file = open(path, "rb")
    return sResponseManager.create_response_200(file, content_type)


@app.route('/cholewp1/z3/')
def index():
    return send_from_directory("static/login.html", "text/html")


@app.route('/cholewp1/z3/register/')
def send_html_register():
    return send_from_directory("static/register.html", "text/html")


@app.route('/cholewp1/z3/css/<path:path>')
def send_css(path):
    return send_from_directory("static/css/" + path, 'text/css')


@app.route('/cholewp1/z3/js/<path:path>')
def send_js(path):
    return send_from_directory("static/js/" + path, 'text/javascript')


@app.route('/cholewp1/z3/img/<path:path>')
def send_img(path):
    return send_from_directory("static/img/" + path, 'image')


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
