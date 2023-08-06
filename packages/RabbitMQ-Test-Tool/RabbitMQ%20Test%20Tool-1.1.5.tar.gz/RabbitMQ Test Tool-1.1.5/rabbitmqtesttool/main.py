from rabbitmqtesttool import commandline, connection as rtt_connection


def main():
    options = commandline.parse_command_line()
    for broker in options.BROKER:
        connection, channel = rtt_connection.open_connection(
            broker, options.vhost, options.user, options.password,
            options.queue, options.durable)
        if connection is None:
            continue
        if options.send:
            print("sending one message")
            channel.basic_publish(exchange="",
                                  routing_key=options.queue,
                                  body=options.send)
            break

        elif options.get:
            print("getting one message")
            method_frame, header_frame, body = channel.basic_get(options.queue)
            if method_frame:
                print("message %s %s '%s'" %
                      (method_frame, message_frame, body.decode("utf-8")))
                channel.basic_ack(method_frame.delivery_tag)
            else:
                print("no message received")

        elif options.list:
            print("message list on broker %s" % broker)
            messages = []
            while True:
                method_frame, header_frame, body = channel.basic_get(
                    options.queue)
                if method_frame:
                    messages.append((method_frame, header_frame, body))
                    channel.basic_ack(method_frame.delivery_tag)
                    print("message %s %s body: '%s'" %
                          (method_frame, header_frame, body.decode("utf-8")))
                else:
                    break
            for _, _, body in messages:
                channel.basic_publish(exchange="",
                                      routing_key=options.queue,
                                      body=body)

        elif options.delete:
            print("deleting queue %s" % options.delete)
            channel.queue_delete(options.delete)
            break

        connection.close()
