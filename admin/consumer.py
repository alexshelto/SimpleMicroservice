# pika used to send events
import pika


params = pika.URLParameters(
    'amqps://tzoklrjp:lDFUDWxOd19WnfvURom5DnVrUK8nhr_x@shrimp.rmq.cloudamqp.com/tzoklrjp',
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(channel, method, properties, body):
    print('received in admin: ')
    print(body)


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
