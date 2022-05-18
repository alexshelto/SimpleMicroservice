# pika used to send events
import json

import pika
from app import db
from app import Product


params = pika.URLParameters(
    'amqps://tzoklrjp:lDFUDWxOd19WnfvURom5DnVrUK8nhr_x@shrimp.rmq.cloudamqp.com/tzoklrjp')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(channel, method, properties, body):
    print('received in main: ')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(
            pk=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product deleted')


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)

print('started consuming')
channel.start_consuming()
channel.close()
