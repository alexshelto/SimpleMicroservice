from products.models import Product  # noreorder
import json
import os

import django
import pika

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')  # noreorder
django.setup()  # noreorder


params = pika.URLParameters(
    'amqps://tzoklrjp:lDFUDWxOd19WnfvURom5DnVrUK8nhr_x@shrimp.rmq.cloudamqp.com/tzoklrjp',
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(channel, method, properties, body):
    print('received in admin: ')
    _id = json.loads(body)
    print(_id)

    if properties.content_type == 'product_liked':
        product = Product.objects.get(id=_id)
        product.likes += 1
        product.save()
        print('Incremented like')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('started consuming')
channel.start_consuming()
channel.close()


"""

ADMIN:
    consumer channel: "ADMIN"
    producer channel: "MAIN"

MAIN:
    consumer channel: "MAIN"

"""
