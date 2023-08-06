import pika


def open_connection(broker, vhost, user, password, queue_name, durable):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=broker,
            virtual_host=vhost,
            credentials=pika.PlainCredentials(user, password)
        ))
    except pika.exceptions.AMQPConnectionError as e:
        print("connection failure for %s: %s" % (broker, e))
        return None, None
    channel = connection.channel()
    channel.queue_declare(queue_name, durable=durable)

    return connection, channel
