#!/usr/bin/env python
import json
from novaclient.client import Client
import pika
import time


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#channel.exchange_declare(exchange='oneview',
#                         type='direct')

channel.queue_declare(queue='oneview_serverprofile_queue', durable=True)
#result = channel.queue_declare(exclusive=True)
#queue_name = result.method.queue

#channel.queue_bind(exchange='oneview',
#                   queue=queue_name,
#                   routing_key='server_profile')

print 'client'
novaclient = Client(2, 'admin', 'nomoresecrete', 'admin',
                    'http://10.4.10.245:5000/v2.0')
print novaclient.flavors.list()
print ' [*] Waiting for new Server Hardware. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] server_hardware:%r" % (body)
    flavor_info = json.loads(body)
    print(flavor_info)
    #novaclient.flavors.create(flavor_name, flavor.ram_mb, flavor.cpus, flavor.disk)
    time.sleep(5)                                                              
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='oneview_serverprofile_queue')

channel.start_consuming()
