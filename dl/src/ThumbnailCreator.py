import os

from src import ConfigManager

__thumbnails_dir = "db/thumbnails/"
__users_dir = "db/userfiles/"

__my_rabbit_id = ConfigManager.get_config("DL_RABBIT_ID")


def create_thumbnail(file_id):
    os.system("/usr/bin/convert " + __users_dir + file_id + " -resize 64x64 " + __thumbnails_dir + file_id)
    return None
