import logging

from flask import render_template
from src import ResponseManager


__page_login = "login.html"


def _create_response_with_resource(path, content_type):
    try:
        file = open("resource/" + path, "rb")
        return ResponseManager.create_response_200(file, content_type)
    except FileNotFoundError as err:
        logging.error(err)
        return ResponseManager.create_response_404()


def send_html(file_name):
    return render_template(file_name)


def send_html_login():
    return render_template(__page_login)


def send_css(file_name):
    return _create_response_with_resource("css/" + file_name, "text/css")


def send_js(file_name):
    return _create_response_with_resource("js/" + file_name, "text/javascript")


def send_img(file_name):
    return _create_response_with_resource("img/" + file_name, "image")
