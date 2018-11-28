import flask

__users_dir = "db/userfiles/"


def get_file(file_id, filename):
    return flask.send_file(
        filename_or_fp=__users_dir + file_id,
        as_attachment=True,
        attachment_filename=filename
    )


def save_user_file(file, file_id):
    file.save(__users_dir + file_id)
    return True
