# pika used to send events
import pika


params = pika.URLParameters(
    'amqps://tzoklrjp:lDFUDWxOd19WnfvURom5DnVrUK8nhr_x@shrimp.rmq.cloudamqp.com/tzoklrjp')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(channel, method, properties, body):
    print('received in main: ')
    print(body)


channel.basic_consume(queue='main', on_message_callback=callback)

print('started consuming')
channel.start_consuming()
channel.close()
