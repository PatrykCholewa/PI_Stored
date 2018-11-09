from flask import Flask, request, flash
from src import ResponseManager, CookieManager, UserFileManager

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4uygkuhjv[$:VHW]'
app.config.update(
    APPLICATION_ROOT="/cholewp1/dl/",
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SECURE=True
)
UserFileManager.init_db()


def validate_user_cookie(cookie, user):
    return cookie is not None and CookieManager.validate_user_jwt(cookie, user)


def validate_file_cookie(cookie, file):
    return cookie is not None and CookieManager.validate_file_by_jwt(cookie, file)


@app.route('/cholewp1/dl/user/<string:user>/list/', methods=['GET'])
def get_file_list(user):
    cookie = request.cookies.get("user")
    if not validate_user_cookie(cookie, user):
        return ResponseManager.create_response_401()

    response = ResponseManager.create_response_200(
        UserFileManager.get_user_file_names(user),
        "application/json")
    CookieManager.set_user_cookie_to_response(response, UserFileManager.get_user_file_ids(user))

    return response


@app.route('/cholewp1/dl/file/<string:file>', methods=['GET'])
def get_file(file):
    cookie = request.cookies.get("file")
    if not validate_file_cookie(cookie, file):
        return ResponseManager.create_response_401()

    try:
        return UserFileManager.get_file(file)
    except FileNotFoundError:
        return ResponseManager.create_response_404()


@app.route('/cholewp1/dl/user/<string:user>/add/', methods=['POST'])
def post_file(user):
    cookie = request.cookies.get("user")
    if not validate_user_cookie(cookie, user):
        return ResponseManager.create_response_401()

    if 'file' not in request.files:
        flash("No file part!")
        return ResponseManager.create_response_400()

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return ResponseManager.create_response_400()

    if UserFileManager.save_user_file(
            user,
            file):
        return ResponseManager.create_response_200(None, None)
    else:
        return ResponseManager.create_response_403()
