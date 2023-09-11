import json
import random

import certifi
import pika

from faker import Faker
from models import User

fake = Faker()
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='notification_service', exchange_type='topic')


def main():
    for _ in range(10):
        full_name = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()[:15]
        notification_method = random.choice(['SMS', 'email'])
        user = User(fullname=full_name, email=email,  phone_number=phone_number, notification_method=notification_method)
        user.save()

        if notification_method == 'SMS':
            queue_name = 'sms_tasks'
        else:
            queue_name = 'email_tasks'

        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange='notification_service', queue=queue_name, routing_key=queue_name)

        channel.basic_publish(
            exchange='notification_service',
            routing_key=queue_name,
            body=str(user.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f"Створено задачу для {user.fullname} в черзі {queue_name}")


    connection.close()


if __name__ == '__main__':
    main()
