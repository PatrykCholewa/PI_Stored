from shutil import copyfile

import flask

from src import ThumbnailCreator

__users_dir = "db/userfiles/"
__thumbnails_dir = "db/thumbnails/"

__default_thumbnail = "resource/default_thumbnail.ico"

__file_ext = ["png", "jpg", "jpeg"]


def get_thumbnail(file_id):
    return flask.send_file(
        filename_or_fp=__thumbnails_dir + file_id
    )


def get_file(file_id, filename):
    return flask.send_file(
        filename_or_fp=__users_dir + file_id,
        as_attachment=True,
        attachment_filename=filename
    )


def save_user_file(file, file_id):
    file.save(__users_dir + file_id)

    if file.filename.split(".")[-1] in __file_ext:
        copyfile(__users_dir + file_id, __thumbnails_dir + file_id)
        ThumbnailCreator.create_thumbnail(file_id)

    return True
