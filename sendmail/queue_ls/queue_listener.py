import json
import pika
import threading
from django.core.mail import send_mail

ROUTING_KEY = 'user.created.key'
EXCHANGE = 'user_exchange'
THREADS = 5

class UserCheckout(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(queue=queue_name, exchange=EXCHANGE, routing_key=ROUTING_KEY)

        self.channel.basic_qos(prefetch_count=THREADS * 10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        try:
            print(properties.content_type)
            if properties.content_type == "user_checkout":
                message = json.loads(body)
                message = json.loads(message)
                print(message)
                subject = 'Welcome to My Site'
                ms = 'Thank you for checkout my shop!'
                from_email = 'admin@mysite.com'
                recipient_list = [message.get('email')]
                send_mail(subject, ms, from_email, recipient_list)
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def run(self):
        print('Inside EmailService : Created Listener ')
        self.channel.start_consuming()
