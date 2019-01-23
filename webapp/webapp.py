from functools import wraps
from six.moves.urllib.parse import urlencode
from authlib.flask.client import OAuth
from flask import Flask, request, session, flash, redirect
from werkzeug.utils import secure_filename

from src import ResourceManager, SessionManager, FileManager, ResponseManager, CookieManager, ConfigManager

__redirect_link_prefix = ConfigManager.get_config("DL_REDIRECT_LINK_PREFIX")
__is_app_secured = ConfigManager.get_config("APP_SECURE")

__application_base_url = ConfigManager.get_config("WEBAPP_APPLICATION_BASE_URL")
__login_callback = ConfigManager.get_config("WEBAPP_LOGIN_CALLBACK")
__user_info_url = ConfigManager.get_config("OAUTH_USER_INFO")
__oauth_client_id = ConfigManager.get_config("OAUTH_CLIENT_ID")

app = Flask(__name__)
app.secret_key = ConfigManager.get_config("APP_SECRET_KEY")
app.config["APPLICATION_ROOT"] = ConfigManager.get_config("APP_APPLICATION_ROOT")
app.config.update(
    SESSION_COOKIE_HTTPONLY=__is_app_secured,
    SESSION_COOKIE_SECURE=__is_app_secured,
    REMEMBER_COOKIE_HTTPONLY=__is_app_secured,
    REMEMBER_COOKIE_SECURE=__is_app_secured
)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=__oauth_client_id,
    client_secret=ConfigManager.get_config("OAUTH_CLIENT_SECRET"),
    api_base_url=ConfigManager.get_config("OAUTH_API_BASE_URL"),
    access_token_url=ConfigManager.get_config("OAUTH_ACCESS_TOKEN_URL"),
    authorize_url=ConfigManager.get_config("OAUTH_AUTHORIZE_URL"),
    client_kwargs={
        'scope': 'openid profile',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'sid' not in session:
            return ResponseManager.create_response_401()

        valid = SessionManager.check_session_valid(session['username'], session['sid'])
        if valid:
            return f(*args, **kwargs)
        else:
            return ResponseManager.create_response_401()

    return decorated


@app.route('/cholewp1/webapp/')
def index():
    return ResourceManager.send_html_login()


@app.route('/cholewp1/webapp/login')
def send_html_login():
    return index()


@app.route('/cholewp1/webapp/user/<string:user>/list')
@requires_auth
def send_html_list(user):
    if user != session['username']:
        return ResponseManager.create_response_400()

    response = ResourceManager.send_html_list(session['username'], FileManager.get_user_file_names(user))
    return CookieManager.set_file_cookie_to_response(response, FileManager.get_user_file_ids(user))


@app.route('/cholewp1/webapp/user/<string:user>/add_file')
@requires_auth
def send_html_add_file(user):
    if user != session['username']:
        return ResponseManager.create_response_400()

    return ResourceManager.send_html_add_file(session['username'])


@app.route('/cholewp1/webapp/css/<path:path>')
def send_css(path):
    return ResourceManager.send_css(path)


@app.route('/cholewp1/webapp/js/<path:path>')
def send_js(path):
    return ResourceManager.send_js(path)


@app.route('/cholewp1/webapp/img/<path:path>')
def send_img(path):
    return ResourceManager.send_img(path)


@app.route('/cholewp1/webapp/manifest/<path:path>')
def send_manifest(path):
    return ResourceManager.send_manifest(path)


@app.route('/cholewp1/webapp/user/<string:user>/file/add', methods=['POST'])
@requires_auth
def get_add_file_access(user):
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

    response = "{\"user\":\"" + user + "\",\"file_id\":\"" + new_file_id + "\",\"filename\":\"" + secure_filename(
        file.filename) + "\"}"
    response = ResponseManager.create_response_200(response, "application/json")
    return CookieManager.set_file_cookie_to_response(response, [new_file_id])


@app.route('/cholewp1/webapp/user/<string:user>/file/<string:file_id>/confirm/<string:filename>', methods=['POST'])
@requires_auth
def add_file_confirm(user, file_id, filename):
    if user != session['username']:
        return ResponseManager.create_response_400()

    res = FileManager.save_user_file_to_db(user, file_id, filename), "text/plain"
    if res:
        return ResponseManager.create_response_200("OK", "text/plain")
    else:
        return ResponseManager.create_response_403()


@app.route('/cholewp1/webapp/user/<string:user>/file/<string:file_id>/share', methods=['POST'])
@requires_auth
def share_file(user, file_id):
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


@app.route('/cholewp1/webapp/oauth')
def login():
    return auth0.authorize_redirect(redirect_uri=__login_callback,
                                    audience=__user_info_url)


@app.route('/cholewp1/webapp/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    username = userinfo['name']

    if 'sid' in session:
        SessionManager.delete_session(session['sid'])

    sid = SessionManager.create_new_session(username)
    session['username'] = username
    session['sid'] = sid

    return ResponseManager.create_response_303(__application_base_url + 'user/' + username + "/list")


@app.route('/cholewp1/webapp/logout/', methods=['GET', 'POST'])
def logout():
    if 'sid' in session:
        SessionManager.delete_session(session['sid'])

    session.clear()

    params = {'returnTo': __application_base_url, 'client_id': __oauth_client_id}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
