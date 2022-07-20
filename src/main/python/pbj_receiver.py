import stomp
import cassis
from threading import Event
from pbj_util import *

exit_event = Event()


def start(queue_name, pbj_user_process, type_system, pbj_sender):
    PbjReceiver(queue_name, pbj_user_process, type_system, pbj_sender)
    while not exit_event.is_set():
        exit_event.wait()


class PbjReceiver(stomp.ConnectionListener):

    def __init__(self, queue_name, jcas_process, type_system, pbj_sender, host_name=DEFAULT_HOST, port_name=DEFAULT_PORT):
        self.source_queue = queue_name
        self.source_host = host_name
        self.source_port = port_name
        self.pbj_sender = pbj_sender
        self.jcas_process = jcas_process
        self.type_system = type_system
        self.conn = stomp.Connection([(self.source_host, self.source_port)])
        self.conn.set_listener('', self)
        self.__connect_and_subscribe()

    def __connect_and_subscribe(self):
        self.conn.connect(DEFAULT_USER, DEFAULT_PASS, wait=True)
        self.conn.subscribe(destination=self.source_queue, id='1', ack='auto')

    def recieve_jcas(self): #IP
        int = 0

    def handleJCas(self): #IP
        int = 0

    def setJCasHandler(self, JCasHandler): #IP
        int = 0

    def set_host(self, host_name): #IP
        self.source_host = host_name

    def stop(self):
        self.conn.disconnect()
        exit_event.set()

    def on_message(self, frame):
        # Here we want a check for some trigger like "PBJ_SHUT_DOWN", and then call __stop.
        if frame.body == STOP_MESSAGE:
            self.stop()
        else:
            cas = cassis.load_cas_from_xmi(frame.body, typesystem=self.type_system)
            self.jcas_process.process_jcas(cas)
            self.pbj_sender.send_jcas(cas)
            print()

    def on_disconnected(self):
        self.__connect_and_subscribe()

    @staticmethod
    def main(self):
        start()
