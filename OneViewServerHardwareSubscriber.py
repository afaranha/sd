#!/usr/bin/env python
import json
#from novaclient.client import Client
from ironicclient import client as ironic_client
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
                   routing_key='server_hardware')

kwargs = {'os_username': 'admin', 'os_password': 'nomoresecrete',
          'os_auth_url': '', 'os_tenant_name': 'admin'}
#ironic = ironic_client.get_client(1, **kwargs)
#novaclient = Client(2, 'admin', 'nomoresecrete', 'admin', args.os_auth_url)
print ' [*] Waiting for new Server Hardware. To exit press CTRL+C'

def _create_ironic_node(server_hardware_info):
    kwargs_node = {
                   'driver': 'pxe_oneview',
                   'properties': {'cpus': server_hardware_info.get('cpus'),
                                  'memory_mb': server_hardware_info.get(
                                                   'memory_mb'),
                                  'local_gb': server_hardware_info.get(
                                                   'local_gb'),
                                  'cpu_arch': 'x86_64'},
                   'extra': {'server_hardware_uri': server_hardware_info.get(
                                                    'server_hardware_uri')},
                  }
    #node = ironic.node.create(**kwargs_node)
    #print('Creating port for Node %(node_uuid)s', {'node_uuid': node.uuid}
    #return node


def callback(ch, method, properties, body):
    print " [x] server_hardware:%r" % (body)
    server_hardware_info = json.loads(body)
    print(server_hardware_info)
    #novaclient.flavors.create(flavor_name, flavor.ram_mb, flavor.cpus, flavor.disk)
    _create_ironic_node(server_hardware_info)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
