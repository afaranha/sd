#!/usr/bin/env python
import json
import pika
import random
import time
import uuid

def create_server_profile_message(cpus, disk, ram_mb, name):
    server_profile = {'cpus': cpus, 'disk': disk, 'ram_mb': ram_mb,
                       'name': name}
    return json.dumps(server_profile)


def create_random_server_profile_message():
    cpus = random.randint(1, 60)
    disk = random.choice([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    ram_mb = random.choice([512, 1024, 2048, 4096, 8192, 16384, 32768,
                               65536])
    name = str(uuid.uuid4())

    return create_server_profile_message(cpus, disk, ram_mb, name)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='oneview',
                         type='direct')

try:
    while True:
        message = create_random_server_profile_message()
        channel.basic_publish(exchange='oneview',
                              routing_key='server_profile',
                              body=message)

        print " [x] Sent server_profile:%r" % (message)
        time.sleep(2)

finally:
    connection.close()
