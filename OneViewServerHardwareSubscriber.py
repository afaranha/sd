#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='oneview',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method_queue

channel.queue_bind(exchange='oneview',
                   queue=queue_name,
                   routing_key='server_hardware')

print ' [*] Waiting for new Server Hardware. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] server_hardware:%r" % (body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
