from flask import Flask, request

app = Flask(__name__)


app = Flask(__name__)
app.secret_key = b'45wh/;ehww4v[$:VHW]'

@app.route('/cholewp1/z3/')
def index():
    return "Jest dobrze"

@app.route('/cholewp1/z3/upload', methods=['POST'])
def upload():
    print(request.files)
    return "OK"
