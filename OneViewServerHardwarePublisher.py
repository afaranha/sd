#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='oneview',
                         type='direct')

message = ' '.join(sys.argv[1:]) or 'New Server Hardware'
channel.basic_publish(exchange='oneview',
                      routing_key='server_hardware',
                      message=message)

print " [x] Sent server_hardware:%r" % (message)
connection.close()
