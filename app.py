from flask import Flask, request, Response

app = Flask(__name__)
app.secret_key = b'45wh/;ehww4v[$:VHW]'


def send_from_directory(content_type, path):
    file = open("static/" + path, "rb")
    response = Response(file)
    response.status = '200 OK'
    response.status_code = 200
    response.content_type = content_type
    return response


@app.route('/cholewp1/z3/')
def index():
    return send_from_directory("text/html", "register.html")


@app.route('/cholewp1/z3/css/<path:path>')
def send_css(path):
    return send_from_directory('text/css', "css/" + path)


@app.route('/cholewp1/z3/js/<path:path>')
def send_js(path):
    return send_from_directory('text/javascript', "js/" + path)


@app.route('/cholewp1/z3/img/<path:path>')
def send_img(path):
    return send_from_directory('image', "img/" + path)
