import argparse
from .type_system_loader import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_USER, DEFAULT_PASS


def get_args():
    parser = argparse.ArgumentParser(
        prog='pbj_sender.py',
        description='Sends...',
        epilog='Text at the bottom of help'
    )
    parser.add_argument('receive_queue')
    parser.add_argument('send_queue')
    parser.add_argument('-hn', '--host_name', default=DEFAULT_HOST)
    parser.add_argument('-pn', '--port_name', default=DEFAULT_PORT)
    parser.add_argument('-u', '--username', default=DEFAULT_USER)
    parser.add_argument('-p', '--password', default=DEFAULT_PASS)

    parser.parse_args()
    args = parser.parse_args()

    return args


