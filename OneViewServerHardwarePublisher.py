#!/usr/bin/env python
import json
import pika
import random
import uuid

def create_server_hardware_message(cpus, memory_mb, local_gb,
                                   server_hardware_uri):
    server_hardware = {'cpus': cpus, 'memory_mb': memory_mb,
                       'local_gb': local_gb,
                       'server_hardware_uri':server_hardware_uri }
    return json.dumps(server_hardware)


def create_random_server_hardware_message():
    cpus = random.randint(1, 60)
    memory_mb = random.choice([512, 1024, 2048, 4096, 8192, 16384, 32768,
                               65536])
    local_gb = random.choice([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    server_hardware_uri = str(uuid.uuid4())

    return create_server_hardware_message(cpus, memory_mb, local_gb,
                                          server_hardware_uri)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='oneview',
                         type='direct')

message = create_random_server_hardware_message()
channel.basic_publish(exchange='oneview',
                      routing_key='server_hardware',
                      body=message)

print " [x] Sent server_hardware:%r" % (message)
connection.close()
