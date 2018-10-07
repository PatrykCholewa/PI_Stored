from werkzeug.wrappers import Request, Response
import matplotlib.image as imgread


def index(request):
    file = open('index.html', encoding='utf-8').read()
    response = Response(file)
    response.content_language = "en"
    response.status = '200 OK'
    response.status_code = 200
    if request.content_type == 'text/html':
        response.content_type = 'text/html; charset=utf-8'
    else:
        response.content_type = 'text/plain; charset=utf-8'

    return response


def css(request):
    file = open(request.path[1:], encoding='utf-8').read()
    response = Response(file)
    response.content_language = "en"
    response.status = '200 OK'
    response.status_code = 200
    response.content_type = 'text/css; charset=utf-8'
    return response

def img(request):
    file = imgread.imread(request.path[1:])
    response = Response(file)
    response.content_language = "en"
    response.status = '200 OK'
    response.status_code = 200
    response.content_type = 'img/ico; charset=utf-8'


@Request.application
def application(request):
    if request.method == 'GET' or request.method == 'POST':

        try:
            file = open(request.path[1:], encoding='utf-8').read()
        except:
            return Response('Internal Server Error', status="500 Internal Server Error")

        response = Response(file)
        if '/css/' in request.path:
            response.content_type = 'text/css'

        response.content_language = "en"
        response.status = '200 OK'
        response.status_code = 200
        if request.content_type == 'text/html' or request.content_type is None:
            response.content_type = 'text/html; charset=utf-8'
        elif request.content_type == 'text/plain':
            response.content_type = 'text/plain; charset=utf-8'
        elif request.content_type == 'text/css':
            response.content_type = 'text/css; charset=utf-8'
        else:
            response = Response('Not implemented content type', status='501 Not Implemented')
    else:
        return Response('Only GET and POST allowed.', status='501 Not Implemented')

    return response


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    app = run_simple('0.0.0.0', 4000, application).wsgi_app()
