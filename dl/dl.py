from flask import Flask, request, session
from src import ResponseManager, CookieManager, UserFileManager

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4uygkuhjv[$:VHW]'
app.config.update(
    APPLICATION_ROOT="/cholewp1/dl/",
    REMEMBER_COOKIE_HTTPONLY=True,
    # REMEMBER_COOKIE_SECURE=True
)


def validate_user_cookie(cookie, user):
    return cookie is not None and CookieManager.validate_user_jwt(cookie, user)


@app.route('/cholewp1/dl/<user>/list/', methods=['GET'])
def get_file_list(user):
    cookie = request.cookies.get("user")
    if not validate_user_cookie(cookie, user):
        return ResponseManager.create_response_401()

    return ResponseManager.create_response_200(
        UserFileManager.get_user_file_names(user),
        "application/json")


@app.route('/cholewp1/dl/<user>/file/<path:path>', methods=['GET'])
def get_file(user, path):
    cookie = request.cookies.get("user")
    if not validate_user_cookie(cookie, user):
        return ResponseManager.create_response_401()

    try:
        return ResponseManager.create_response_200(
            UserFileManager.get_user_file(user, path),
            'application/octet-stream'
        )
    except FileNotFoundError:
        return ResponseManager.create_response_404()


# @app.route('/cholewp1/z3/ws/files/add/', methods=['POST'])
# def post_file():
#     if is_not_logged():
#         return ResponseManager.create_response_401()
#
#     if 'file' not in request.files:
#         flash("No file part!")
#         return ResponseManager.create_response_400()
#
#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file')
#         return ResponseManager.create_response_400()
#
#     if UserFileManager.save_user_file(
#             session['username'],
#             file):
#         return ResponseManager.create_response_200(None, None)
#     else:
#         return ResponseManager.create_response_403()
#
