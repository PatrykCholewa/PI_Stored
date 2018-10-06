from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    request_data = request.stream.read()
    input_argument = -1
    if len(request_data) > 0:
        try:
            input_argument = int(request_data)
        except ValueError:
            input_argument = -2
    
    return Response('Twoja liczba to %d' % input_argument, status='200 OK')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = run_simple('127.0.0.1', 4000, application).wsgi_app()
