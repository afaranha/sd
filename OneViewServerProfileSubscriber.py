#!/usr/bin/env python
import json
from novaclient.client import Client
import pika
import time


parameters = pika.URLParameters('amqp://admin:root@1r0n1c@10.4.10.244:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


channel.queue_declare(queue='oneview_serverprofile_queue', durable=True)

novaclient = Client(2, 'admin', 'nomoresecrete', 'admin',
                    'http://10.4.10.245:5000/v2.0')
print ' [*] Waiting for new Server Profile. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] server_profile:%r" % (body)
    flavor_info = json.loads(body)
    print(flavor_info)
    novaclient.flavors.create(flavor_info.get('name'), flavor_info.get('ram_mb'), flavor_info.get('cpus'), flavor_info.get('disk'))
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='oneview_serverprofile_queue')

channel.start_consuming()
