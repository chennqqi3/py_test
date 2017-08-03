# coding=utf-8
import pika

creds_broker = pika.PlainCredentials("admin", "mUu8al5f")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.5.162',
                                                               port=5672,
                                                               virtual_host="/",
                                                               credentials=creds_broker))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode = 2, # make message persistent
                      ))
print " [x] Sent %r" % (message,)
connection.close()