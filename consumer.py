import pika
from django.conf import settings

def callback(ch, method, properties, body):
    # Process the incoming message
    print('properties:-', properties)
    print(f"Received message: {body}")

def consume_messages():
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=pika.PlainCredentials(
                'ram', 'ram'
            ),
        )
    )

    # Create a channel
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='django_project')

    # Set up a message consumer
    channel.basic_consume(queue='django_project', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. from abstractuser_project*******************')
    channel.start_consuming()

# Example usage:
consume_messages()
