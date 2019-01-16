#!/usr/bin/env python
import pika
from uuid import uuid4

body = '/tmp/image{}.png'.format(uuid4())

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='thumbnail.png', durable=True)

channel.basic_publish(exchange='',
                      routing_key='thumbnail.png',
                      body=body)
print(" [x] Sent '{}'".format(body))
connection.close()
