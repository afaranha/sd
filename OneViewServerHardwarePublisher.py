#!/usr/bin/env python
import json
import pika
import random
import sys
import time
import uuid

def create_server_hardware_message(cpus, memory_mb, local_gb,
                                   server_hardware_uri):
    server_hardware = {'cpus': cpus, 'memory_mb': memory_mb,
                       'local_gb': local_gb,
                       'server_hardware_uri':server_hardware_uri }
    return json.dumps(server_hardware)


def create_random_server_hardware_message():
    cpus = random.choice([1, 2, 4, 8, 16, 32, 64, 128])
    memory_mb = random.choice([512, 1024, 2048, 4096, 8192, 16384, 32768,
                               65536])
    local_gb = random.choice([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    server_hardware_uri = str(uuid.uuid4())

    return create_server_hardware_message(cpus, memory_mb, local_gb,
                                          server_hardware_uri)


parameters = pika.URLParameters('amqp://admin:root@1r0n1c@10.4.10.244:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='oneview_serverhardware_queue', durable=True)

number_of_serverhardware = sys.argv[1:2] or ['1']
number_of_serverhardware = int(number_of_serverhardware[0])
print "Sending %s Server Hardware" % number_of_serverhardware

try:
    while (number_of_serverhardware > 0):
        message = create_random_server_hardware_message()
        channel.basic_publish(exchange='',
                              routing_key='oneview_serverhardware_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))

        print " [x] Sent server_hardware:%r" % (message)
        time.sleep(2)
        number_of_serverhardware = number_of_serverhardware -1

finally:
    connection.close()
