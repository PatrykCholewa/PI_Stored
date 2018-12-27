import logging

from flask import render_template
from src import ResponseManager


__page_login = "login.html"
__page_list = "list.html"
__page_add_file = "add_file.html"


def __create_response_with_resource(path, content_type):
    try:
        file = open("resource/" + path, "rb")
        return ResponseManager.create_response_200(file, content_type)
    except FileNotFoundError as err:
        logging.error(err)
        return ResponseManager.create_response_404()


def send_html_login():
    return render_template(__page_login)


def send_html_list(username):
    return render_template(__page_list, username=username)


def send_html_add_file(username):
    return render_template(__page_add_file, username=username)


def send_css(file_name):
    return __create_response_with_resource("css/" + file_name, "text/css")


def send_js(file_name):
    return __create_response_with_resource("js/" + file_name, "text/javascript")


def send_img(file_name):
    return __create_response_with_resource("img/" + file_name, "image")
