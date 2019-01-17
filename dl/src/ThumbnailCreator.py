#!/usr/bin/env python
import pika

from src import ConfigManager

__thumbnails_dir = "db/thumbnails/"

__my_rabbit_id = ConfigManager.get_config("DL_RABBIT_ID")


def send_thumbnail_request(body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange=__my_rabbit_id, durable=True)
    channel.basic_publish(__my_rabbit_id, __my_rabbit_id, body)

    print(" [x] Sent '{}'".format(body))
    connection.close()


def create_thumbnail(file_id):
    send_thumbnail_request(file_id)
    return None
