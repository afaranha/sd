#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='oneview_publisher',
                         type='direct')

message = ' '.join(sys.argv[1:]) or 'New Server Hardware'
channel.basic_publish(exchange='oneview_publisher',
                      routing_key='server_hardware',
                      message=message)

print " [x] Sent server_hardware:%r" % (message)
connection.close()
