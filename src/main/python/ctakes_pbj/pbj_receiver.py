import time
from threading import Event
import stomp
from .type_system_loader import *
from ctakes_pbj.cas_handlers.pbj_pipeline import STOP_MESSAGE
from ctakes_pbj import arg_parser
args = arg_parser.get_args()

exit_event = Event()


def start_receiver(pipeline, queue_name=args.receive_queue, host_name=args.host_name, port_name=args.port_name):
    PBJReceiver(pipeline, queue_name, host_name, port_name)
    while not exit_event.is_set():
        exit_event.wait()


class PBJReceiver(stomp.ConnectionListener):

    def __init__(self, pipeline, queue_name, host_name, port_name):
        self.source_queue = queue_name
        self.source_host = host_name
        self.source_port = port_name
        self.pipeline = pipeline
        self.typesystem = None
        self.conn = stomp.Connection([(self.source_host, self.source_port)])
        self.conn.set_listener('', self)
        self.stop = False
        self.__connect_and_subscribe()
        # self.waiting_for_message()

    def __connect_and_subscribe(self):
        self.conn.connect(DEFAULT_USER, DEFAULT_PASS, wait=True)
        self.conn.subscribe(destination=self.source_queue, id='1', ack='auto')

    def set_typesystem(self, typesystem):
        self.typesystem = typesystem

    def get_typesystem(self):
        if self.typesystem is None:
            # Load the typesystem
            type_system_accessor = TypeSystemLoader()
            type_system_accessor.load_type_system()
            self.set_typesystem(type_system_accessor.get_type_system())
            print("typesystem print")

        return self.typesystem

    def set_host(self, host_name):
        self.source_host = host_name

    def set_stop(self, stop):
        self.stop = stop

    def stop_receiver(self):
        self.conn.disconnect()
        self.pipeline.collection_process_complete()
        exit_event.set()

    def on_message(self, frame):
        # Here we want a check for some trigger like "PBJ_SHUT_DOWN", and then call __stop.
        if frame.body == STOP_MESSAGE:
            self.stop = True
            time.sleep(3)
            self.stop_receiver()
            print("\nReceiver stopped")
        else:
            # should we just stop the receiver after one sent message or keep it open for multiple messages?

            if XMI_INDICATOR in frame.body:
                print("got xmi")
                cas = cassis.load_cas_from_xmi(frame.body, self.get_typesystem())
                print("cas loaded")
                self.pipeline.process(cas)
                print("cas processed")
            else:
                print(frame.body)

    def on_disconnected(self):
        self.__connect_and_subscribe()

