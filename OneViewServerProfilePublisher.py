#!/usr/bin/env python
import json
import pika
import random
import sys
import time
import uuid

def create_server_profile_message(cpus, disk, ram_mb, name):
    server_profile = {'cpus': cpus, 'disk': disk, 'ram_mb': ram_mb,
                       'name': name}
    return json.dumps(server_profile)


def create_random_server_profile_message():
    cpus = random.choice([1, 2, 4, 8, 16, 32, 64, 128])
    disk = random.choice([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    ram_mb = random.choice([512, 1024, 2048, 4096, 8192, 16384, 32768,
                               65536])
    name = str(uuid.uuid4())

    return create_server_profile_message(cpus, disk, ram_mb, name)


parameters = pika.URLParameters('amqp://admin:root@1r0n1c@10.4.10.244:5672/%2F')
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='oneview_serverprofile_queue', durable=True)

number_of_serverprofile = sys.argv[1:2] or ['1']
number_of_serverprofile = int(number_of_serverprofile[0])
print "Sending %s Server Profile" % number_of_serverprofile

try:
    while number_of_serverprofile > 0:
        message = create_random_server_profile_message()
        channel.basic_publish(exchange='',
                              routing_key='oneview_serverprofile_queue',
                              body=message,
                              properties=pika.BasicProperties(                 
                                  delivery_mode=2                              
                              ))

        print " [x] Sent server_profile:%r" % (message)
        time.sleep(2)
        number_of_serverprofile = number_of_serverprofile - 1

finally:
    connection.close()
