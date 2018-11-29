from flask import Flask, request, session, flash
from werkzeug.utils import secure_filename

from src import ResourceManager, UserManager, FileManager, ResponseManager, CookieManager

__page_login = "login.html"
__page_register = "register.html"
__page_list = "list.html"
__page_add_file = "add_file.html"

__redirect_link_prefix = "https://pi.iem.pw.edu.pl/cholewp1/dl/file/"

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

    return not UserManager.check_session_valid(session['username'], session['sid'])


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


@app.route('/cholewp1/webapp/user/<string:username>/list')
def send_html_list(username):
    if is_not_logged():
        return ResponseManager.create_response_401()

    return ResourceManager.send_html(__page_list)


@app.route('/cholewp1/webapp/user/<string:username>/add_file')
def send_html_add_file(username):
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


@app.route('/cholewp1/webapp/user/<string:user>/file/list', methods=['GET'])
def get_user_files(user):
    if is_not_logged():
        return ResponseManager.create_response_401()

    if user != session['username']:
        return ResponseManager.create_response_400()

    response = ResponseManager.create_response_200(FileManager.get_user_file_names(user), "application/json")
    return CookieManager.set_file_cookie_to_response(response, FileManager.get_user_file_ids(user))


@app.route('/cholewp1/webapp/user/<string:user>/file/add', methods=['POST'])
def get_add_file_access(user):
    if is_not_logged():
        return ResponseManager.create_response_401()

    if user != session['username']:
        return ResponseManager.create_response_400()

    if 'file' not in request.files:
        flash("No file part!")
        return ResponseManager.create_response_400()

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return ResponseManager.create_response_400()

    new_file_id = FileManager.get_new_file_id(user)

    response = "{\"user\":\""+user+"\",\"file_id\":\""+new_file_id+"\",\"filename\":\""+secure_filename(file.filename)+"\"}"
    response = ResponseManager.create_response_200(response, "application/json")
    return CookieManager.set_file_cookie_to_response(response, [new_file_id])


@app.route('/cholewp1/webapp/user/<string:user>/file/<string:file_id>/confirm/<string:filename>', methods=['POST'])
def add_file_confirm(user, file_id, filename):
    if is_not_logged():
        return ResponseManager.create_response_401()

    if user != session['username']:
        return ResponseManager.create_response_400()

    res = FileManager.save_user_file_to_db(user, file_id, filename), "text/plain"
    if res:
        return ResponseManager.create_response_200("OK", "text/plain")
    else:
        return ResponseManager.create_response_403()


@app.route('/cholewp1/webapp/user/<string:user>/file/<string:file_id>/share', methods=['POST'])
def share_file(user, file_id):
    if is_not_logged():
        return ResponseManager.create_response_401()

    if user != session['username']:
        return ResponseManager.create_response_400()

    if FileManager.is_file_shared(file_id):
        return ResponseManager.create_response_403()

    FileManager.set_file_shared(file_id)

    return ResponseManager.create_response_200(None, None)


@app.route('/cholewp1/webapp/share/file/<string:file_id>', methods=['GET'])
def get_shared_file(file_id):

    res = FileManager.is_file_shared(file_id)

    if res:
        filename = FileManager.get_file_name_by_id(file_id)
        response = ResponseManager.create_response_303(__redirect_link_prefix + file_id + "/name/" + filename)
        return CookieManager.set_file_cookie_to_response(response, [file_id])
    else:
        return ResponseManager.create_response_403()


@app.route('/cholewp1/webapp/ws/login/', methods=['POST'])
def login():
    username = request.form['user-id']
    if UserManager.authenticate_user(username, request.form['password']):
        sid = UserManager.create_new_session(username)
        session['username'] = username
        session['sid'] = sid

        response = ResourceManager.send_html(__page_list)
        return response
    else:
        ResponseManager.create_response_401()


@app.route('/cholewp1/webapp/ws/logout/', methods=['POST'])
def logout():
    if is_not_logged():
        return ResponseManager.create_response_401()

    UserManager.delete_session(session['username'])
    session.pop('sid', None)
    session.pop('username', None)
    return ResourceManager.send_html(__page_login)


@app.route('/cholewp1/webapp/ws/register/', methods=['POST'])
def register():
    # return ResponseManager.create_response_403()
    # AVAILABLE BECAUSE OF OFTEN DB CLEARING
    new_user = UserManager.add_new_user(request.form['user-id'], request.form['password'])
    if new_user is not None:
        return ResourceManager.send_html(__page_login)
    else:
        return ResponseManager.create_response_401()


# DATABASE CLEARING PROTECTION
if __name__ == '__main__':
    UserManager.add_new_user("cholewp1", "test")
    UserManager.add_new_user("cholewp2", "test")
    FileManager.init_db()
