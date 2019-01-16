#!/usr/bin/env python
import pika
from uuid import uuid4

from src import ConfigManager

body = '/tmp/image{}.png'.format(uuid4())

my_rabbit_id = ConfigManager.get_config("DL_RABBIT_ID")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange=my_rabbit_id, durable=True)
channel.basic_publish(my_rabbit_id, my_rabbit_id, body)

print(" [x] Sent '{}'".format(body))
connection.close()
