#!/usr/bin/env python
import pika

from src import ConfigManager

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
my_rabbit_id = ConfigManager.get_config("DL_RABBIT_ID")


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.queue_declare(queue=my_rabbit_id, durable=True)
channel.queue_bind(queue=my_rabbit_id, exchange=my_rabbit_id, routing_key=my_rabbit_id)
channel.basic_consume(callback, my_rabbit_id)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
