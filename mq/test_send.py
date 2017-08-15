# coding=utf-8
import pika

creds_broker = pika.PlainCredentials("admin", "mUu8al5f")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.5.162',
                                                               port=5672,
                                                               virtual_host="/",
                                                               credentials=creds_broker))
channel = connection.channel()

message = 'hello eee'

if __name__ == '__main__':
    channel.basic_publish(exchange='task_exchange', routing_key='task_test', body=message,
                         properties=pika.BasicProperties(
                             # make message persistent
                             delivery_mode=2, content_encoding='UTF-8',content_type='text/plain'
                         )
                         )