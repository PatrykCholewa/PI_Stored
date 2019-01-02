import logging

from flask import render_template
from src import ResponseManager


__page_login = "login.html"
__page_list = "list.html"
__page_add_file = "add_file.html"


def __is_adding_files_allowed(files):
    return len(files) < 5


def __create_response_with_resource(path, content_type):
    try:
        file = open("resource/" + path, "rb")
        return ResponseManager.create_response_200(file, content_type)
    except FileNotFoundError as err:
        logging.error(err)
        return ResponseManager.create_response_404()


def send_html_login():
    return ResponseManager.create_response_200(
        render_template(__page_login),
        "text/html"
    )


def send_html_list(username, files):
    return ResponseManager.create_response_200(
        render_template(__page_list,
                        username=username,
                        files=files,
                        add_file_visible=__is_adding_files_allowed(files)),
        "text/html"
    )


def send_html_add_file(username):
    return ResponseManager.create_response_200(
        render_template(__page_add_file,
                        username=username,
                        add_file_visible=True),
        "text/html"
    )


def send_css(file_name):
    return __create_response_with_resource("css/" + file_name, "text/css")


def send_js(file_name):
    return __create_response_with_resource("js/" + file_name, "text/javascript")


def send_img(file_name):
    return __create_response_with_resource("img/" + file_name, "image")


def send_manifest(file_name):
    return __create_response_with_resource("manifest/" + file_name, None)
