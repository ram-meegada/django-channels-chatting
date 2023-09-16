import pika, json
from django.conf import settings

def publish_message(method, message):
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
    properties = pika.BasicProperties(method)
    channel = connection.channel()

    channel.queue_declare(queue='django_project')
    message = json.dumps(message)
    # Publish the message
    channel.basic_publish(exchange='', routing_key='django_project', body=message, properties=properties)

    # Close the connection
    connection.close()

# Example usage:
# message = "Hello, RabbitMQ!"
# publish_message(message)
