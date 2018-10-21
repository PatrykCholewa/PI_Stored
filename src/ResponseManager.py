from flask import Response, abort


def _create_response(content, content_type, status_code, status):
    __response = Response(content)
    __response.content_type = content_type
    __response.status_code = status_code
    __response.status = status
    return __response


def create_response_200(content, content_type):
    return _create_response(content, content_type, 200, "200 OK")


def create_response_401():
    return abort(401)


def create_response_404():
    return abort(404)


def create_response_403():
    return abort(403)
