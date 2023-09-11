import json
import certifi
import pika

from faker import Faker
from models import User

fake = Faker()
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='email_service', exchange_type='direct')
channel.queue_declare(queue='email_tasks', durable=True)
channel.queue_bind(exchange='email_service', queue="email_tasks")


def main():
    for _ in range(10):
        full_name = fake.name()
        email = fake.email()
        user = User(fullname=full_name, email=email)
        user.save()

        channel.basic_publish(
            exchange='email_service',
            routing_key='email_tasks',
            body=str(user.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    connection.close()


if __name__ == '__main__':
    main()
