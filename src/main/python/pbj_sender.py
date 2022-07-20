import stomp
from pbj_util import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_USER, DEFAULT_PASS


class PBJSender:

    def __init__(self, queue_name, host_name=DEFAULT_HOST, port_name=DEFAULT_PORT, password=DEFAULT_PASS, username=DEFAULT_USER):
        self.target_queue = queue_name
        self.target_host = host_name
        self.target_port = port_name
        self.password = password
        self.username = username

    def send_jcas(self, cas):
        xmi = cas.to_xmi()
        conn = stomp.Connection([(self.target_host, self.target_port)])
        conn.connect(self.username, self.password, wait=True)
        conn.send(self.target_queue, xmi)
        print("sent to: " + self.target_queue)

    @staticmethod
    def send_stop(self):
        #something
        int =0

    def set_queue(self, queue_name):
        self.target_queue = queue_name

    def set_host(self, host_name):
        self.target_host = host_name

    def set_port(self, port_name):
        self.target_port = port_name

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

