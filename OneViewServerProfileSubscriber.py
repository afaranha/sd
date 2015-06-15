#!/usr/bin/env python
import json
from novaclient.client import Client
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='oneview',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='oneview',
                   queue=queue_name,
                   routing_key='server_profile')

#novaclient = Client(2, 'admin', 'nomoresecrete', 'admin', args.os_auth_url)
print ' [*] Waiting for new Server Hardware. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] server_hardware:%r" % (body)
    flavor_info = json.loads(body)
    print(flavor_info)
    #novaclient.flavors.create(flavor_name, flavor.ram_mb, flavor.cpus, flavor.disk)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
