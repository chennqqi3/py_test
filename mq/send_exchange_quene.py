# coding=utf-8
import pika

creds_broker = pika.PlainCredentials("admin", "mUu8al5f")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.5.162',
                                                               port=5672,
                                                               virtual_host="/",
                                                               credentials=creds_broker))
channel = connection.channel()

# Direct类型的exchange, 名称 pdf_events
channel.exchange_declare(exchange='pdf_events', exchange_type='direct', durable = True, auto_delete=False, arguments=None)

# 创建create_pdf_queue队列
channel.queue_declare(queue='create_pdf_queue', durable=True, exclusive = False, auto_delete=False, arguments=None)

# 创建 pdf_log_queue队列
channel.queue_declare(queue='pdf_log_queue', durable=True, exclusive = False, auto_delete=False, arguments=None)

# 绑定 pdf_events --> create_pdf_queue 使用routingkey:pdf_create
channel.queue_bind(queue='create_pdf_queue', exchange='pdf_events',routing_key='pdf_events',arguments= None)

# 绑定 pdf_events --> pdf_log_queue 使用routingkey:pdf_log
channel.queue_bind(queue='pdf_log_queue', exchange='pdf_events',routing_key='pdf_log',arguments= None)

message = "Demo some pdf creating..."

# 发送消息到exchange :pdf_events ,使用routingkey: pdf_create
# 通过binding routinekey的比较，次消息会路由到队列 create_pdf_queue
channel.BasicPublish(exchange='pdf_events',
                     routing_key='pdf_create',
                     body=message,
                     properties=pika.BasicProperties(
                        # make message persistent
                        delivery_mode=2
                    )
                    )

message = "pdf loging ...";

# 发送消息到exchange :pdf_events ,使用routingkey: pdf_log
# 通过binding routinekey的比较，次消息会路由到队列 pdf_log_queue
channel.BasicPublish(exchange='pdf_events',
                     routing_key='pdf_log',
                     body=message,
                     properties=pika.BasicProperties(
                         # make message persistent
                         delivery_mode=2
                     )
                     )
