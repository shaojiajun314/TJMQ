from pickle import dumps as p_dumps

from TJQueue.queue import get_queue
from .protocol import Protocol, Header


class AuthError(Exception):
    pass


class AbstractClient():
    def __init__(self, ip, port, from_queue=False):
        self.from_queue = from_queue

    def push(self, queue, data):
        raise NotImplementedError()

    def pop(self, queue):
        if self.from_queue:
            return get_queue(queue).pop()
        else:
            return self.get_from_net(queue)

    def protocol(self, msg, write=None):
        p = Protocol(msg)
        q = get_queue(p.header.qname)
        if p.header.method == Header.RESPONSE:
            return p

    def send_auth(self):
        return p_dumps('auth msg').hex().encode()

    def get_from_net(self, queue_name):
        raise NotImplementedError()

    def close(self):
        pass
