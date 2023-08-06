import argparse


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "BROKER",
        help="The IP address or hostname of the broker, default = %(default)s",
        default="localhost",
        nargs="+")
    parser.add_argument(
        "--durable",
        action="store_true")
    parser.add_argument(
        "--queue",
        help="The queue to use, default = %(default)s",
        type=str,
        default="test_queue")
    parser.add_argument(
        "--send",
        metavar="MSG",
        help="Send MSG to queue")
    parser.add_argument(
        "--get",
        help="Get one message from queue",
        action="store_true")
    parser.add_argument(
        "--list",
        help="List messages in queue",
        action="store_true")
    parser.add_argument(
        "--user",
        help="The user to use for the RabbitMQ connection, "
        "default = %(default)s",
        default="tester")
    parser.add_argument(
        "--password",
        help="The password to use for the RabbitMQ connection, "
        "default = %(default)s",
        default="linux")
    parser.add_argument(
        "--vhost",
        help="The vhost to use for the RabbitMQ connection, "
        "default = %(default)s",
        default="tester")
    parser.add_argument(
        "--delete",
        metavar="QUEUE",
        help="Delete QUEUE")
    return parser.parse_args()
