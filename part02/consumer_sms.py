import pika

from models import User

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='sms_tasks', durable=True)


def send_sms_fake(phone_number):
    print(f"Відправка sms на номер {phone_number}")


def callback(ch, method, properties, body):
    pk = body.decode()
    user = User.objects(id=pk, completed=False, notification_method="SMS").first()
    if user:
        user_phone = user.phone_number
        send_sms_fake(user_phone)
        user.update(set__completed=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='sms_tasks', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()
