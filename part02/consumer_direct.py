import pika

from models import User

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_tasks', durable=True)


def send_email_fake(user_email):
    print(f"Відправка електронного листа на {user_email}")


def callback(ch, method, properties, body):
    pk = body.decode()
    user = User.objects(id=pk, completed=False).first()
    if user:
        user_email = user.email
        send_email_fake(user_email)
        user.update(set__completed=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_tasks', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()
