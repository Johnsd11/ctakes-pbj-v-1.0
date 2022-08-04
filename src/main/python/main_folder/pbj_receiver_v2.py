import sys
from threading import Event
import stomp
import time
from pbj_util import *

exit_event = Event()


def start_receiver(queue_name):
    PbjReceiver(queue_name)
    while not exit_event.is_set():
        exit_event.wait()


class PbjReceiver(stomp.ConnectionListener):

    def __init__(self, queue_name, host_name=DEFAULT_HOST, port_name=DEFAULT_PORT):
        self.source_queue = queue_name
        self.source_host = host_name
        self.source_port = port_name
        self.conn = stomp.Connection([(self.source_host, self.source_port)])
        self.conn.set_listener('', self)
        self.stop = False
        self.__connect_and_subscribe()
        self.waiting_for_message()

    def __connect_and_subscribe(self):
        self.conn.connect(DEFAULT_USER, DEFAULT_PASS, wait=True)
        self.conn.subscribe(destination=self.source_queue, id='1', ack='auto')

    def receive_jcas(self): #IP
        int = 0

    def handle_jcas(self): #IP
        int = 0

    def set_jcas_handler(self, JCasHandler): #IP
        int = 0

    def set_host(self, host_name): #IP
        self.source_host = host_name

    def set_stop(self, stop):
        self.stop = stop

    def stop_receiver(self):
        self.conn.disconnect()
        #self.pbj_sender.send_stop()
        exit_event.set()

    def waiting_for_message(self):
        while not self.stop:
            for x in range(0, 4):
                b = "Waiting for Sender" + "." * x
                print("\r", b, end="")
                time.sleep(1)

    def on_message(self, frame):
        # Here we want a check for some trigger like "PBJ_SHUT_DOWN", and then call __stop.
        if frame.body == STOP_MESSAGE:
            self.stop = True
            time.sleep(3)
            self.stop_receiver()
            print("\nReceiver stopped")
        else:
            # should we just stop the receiver after one sent message or keep it open for multiple messages?

            # cas = cassis.load_cas_from_xmi(frame.body, typesystem=self.type_system)
            # self.jcas_process.process_jcas(cas)
            # self.pbj_sender.send_jcas(cas)

            # need to get

            print("blah")

    def on_disconnected(self):
        self.__connect_and_subscribe()

    @staticmethod
    def main(self):
        start_receiver()
