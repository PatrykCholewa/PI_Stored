#!/usr/bin/env python
import os

import pika

from src import ConfigManager

__users_dir = "db/userfiles/"
__thumbnails_dir = "db/thumbnails/"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
my_rabbit_id = ConfigManager.get_config("DL_RABBIT_ID")


def callback(ch, method, properties, body):
    body = body.decode("utf-8")
    print(" [x] Received %r" % body)
    try:
        os.system("/usr/bin/convert " + __users_dir + body + " -resize 64x64 " + __thumbnails_dir + body)
    except Exception as e:
        print(e)
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.queue_declare(queue=my_rabbit_id, durable=True)
channel.queue_bind(queue=my_rabbit_id, exchange=my_rabbit_id, routing_key=my_rabbit_id)
channel.basic_consume(callback, my_rabbit_id)

print(' [*] Waiting for messages.')
channel.start_consuming()
