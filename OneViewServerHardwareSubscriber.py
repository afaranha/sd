#!/usr/bin/env python
import json
from ironicclient import client as ironic_client
import pika
import time


parameters = pika.URLParameters('amqp://admin:root@1r0n1c@10.4.10.244:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


channel.queue_declare(queue='oneview_serverhardware_queue', durable=True)

kwargs = {'os_username': 'admin', 'os_password': 'nomoresecrete',
          'os_auth_url': 'http://10.4.10.245:5000/v2.0', 'os_tenant_name': 'admin'}
ironic = ironic_client.get_client(1, **kwargs)

print ' [*] Waiting for new Server Hardware. To exit press CTRL+C'

def _create_ironic_node(server_hardware_info):
    kwargs_node = {
                   'driver': 'fake',
                   'properties': {'cpus': server_hardware_info.get('cpus'),
                                  'memory_mb': server_hardware_info.get(
                                                   'memory_mb'),
                                  'local_gb': server_hardware_info.get(
                                                   'local_gb'),
                                  'cpu_arch': 'x86_64'},
                   'extra': {'server_hardware_uri': server_hardware_info.get(
                                                    'server_hardware_uri')},
                  }
    node = ironic.node.create(**kwargs_node)
    print('Creating port for Node %(node_uuid)s', {'node_uuid': node.uuid})
    return node


def callback(ch, method, properties, body):
    print " [x] server_hardware:%r" % (body)
    server_hardware_info = json.loads(body)
    print(server_hardware_info)
    _create_ironic_node(server_hardware_info)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='oneview_serverhardware_queue')

channel.start_consuming()
