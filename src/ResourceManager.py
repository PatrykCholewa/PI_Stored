import logging
from src import ResponseManager


def _create_response_with_resource(path, content_type):
    try:
        file = open("resource/" + path, "rb")
        return ResponseManager.create_response_200(file, content_type)
    except FileNotFoundError as err:
        logging.error(err)
        return ResponseManager.create_response_404()


def send_html(file_name):
    return _create_response_with_resource(file_name, "text/html")


def send_css(file_name):
    return _create_response_with_resource("css/" + file_name, "text/css")


def send_js(file_name):
    return _create_response_with_resource("js/" + file_name, "text/javascript")


def send_img(file_name):
    return _create_response_with_resource("img/" + file_name, "image")


def send_html_template(file_name):
    return _create_response_with_resource("template/" + file_name, "text/html")
