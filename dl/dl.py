from flask import Flask, request, flash
from src import ResponseManager, CookieManager, UserFileManager, ConfigManager

app = Flask(__name__)
app.secret_key = ConfigManager.get_config("APP_SECRET_KEY")
app.config.update(
    APPLICATION_ROOT=ConfigManager.get_config("APP_APPLICATION_ROOT"),
    REMEMBER_COOKIE_HTTPONLY=ConfigManager.get_config("APP_SECURE"),
    REMEMBER_COOKIE_SECURE=ConfigManager.get_config("APP_SECURE")
)


def validate_user_cookie(cookie, user):
    return cookie is not None and CookieManager.validate_user_jwt(cookie, user)


def validate_file_cookie(cookie, file):
    return cookie is not None and CookieManager.validate_file_by_jwt(cookie, file)


@app.route('/cholewp1/dl/file/<string:file_id>/name/<string:filename>', methods=['GET'])
def get_file(file_id, filename):
    cookie = request.cookies.get("file")
    if not validate_file_cookie(cookie, file_id):
        return ResponseManager.create_response_401()

    try:
        return UserFileManager.get_file(file_id, filename)
    except FileNotFoundError:
        return ResponseManager.create_response_404()


@app.route('/cholewp1/dl/file/<string:file_id>', methods=['POST'])
def post_file(file_id):
    cookie = request.cookies.get("file")
    if not validate_file_cookie(cookie, file_id):
        return ResponseManager.create_response_401()

    if 'file' not in request.files:
        flash("No file part!")
        return ResponseManager.create_response_400()

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return ResponseManager.create_response_400()

    if UserFileManager.save_user_file(
            file,
            file_id):
        return ResponseManager.create_response_200(None, None)
    else:
        return ResponseManager.create_response_403()
