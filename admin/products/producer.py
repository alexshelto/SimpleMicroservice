# pika used to send events
import pika


params = pika.URLParameters(
    'amqps://tzoklrjp:lDFUDWxOd19WnfvURom5DnVrUK8nhr_x@shrimp.rmq.cloudamqp.com/tzoklrjp',
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish():
    channel.basic_publish(exchange='', routing_key='main', body='hello',)
