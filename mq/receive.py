# coding=utf-8

import pika
import time

creds_broker = pika.PlainCredentials("admin", "mUu8al5f")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.5.162',
                                                               port=5672,
                                                               virtual_host="/",
                                                               credentials=creds_broker))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep( body.count('.') )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)

# 通过 basic.qos 方法设置prefetch_count=1 。这样RabbitMQ就会使得每个Consumer在同一个时间点最多处理一个Message。换句话说，在接收到该Consumer的ack前，他它不会将新的Message分发给它
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()