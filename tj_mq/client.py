import asyncio
from queue import Queue
from threading import Thread

from .utils import readpkg
from ..protocol import Protocol, Header, ProtocolError
from ..abstract_client import AbstractClient, AuthError


class Client(AbstractClient):
    def __init__(self, ip, port, from_queue=False):
        super().__init__(ip, port, from_queue)
        self.ip = ip
        self.port = port
        self.reader = None
        self.writer = None
        self.data_cache = Queue()
        self.stop = False
        self.loop = None
        if not self.from_queue:
            self.net_queue_map = {}
        Thread(target=self.run, daemon=True).start()

    def push(self, queue, data):
        self.data_cache.put(Protocol.build_request(Header.PUSH, queue.encode(), data))

    async def open_connection(self):
        self.reader, self.writer = await asyncio.open_connection(
            host = self.ip,
            port = self.port,
        )
        auth_msg = self.send_auth()
        if not isinstance(auth_msg, bytes):
            auth_msg = auth_msg.encode()
        self.writer.write(auth_msg)
        self.writer.write(b'\r\n')
        ret = (await self.reader.readline()).strip()
        if ret == b'ok':
            return
        raise AuthError('error auth')

    async def client_write_loop(self):
        while 1:
            if self.data_cache.empty():
                if self.stop:
                    return
                await asyncio.sleep(0.05)
                continue
            d = self.data_cache.get()
            self.writer.write(f'{len(d)}\r\n'.encode())
            self.writer.write(d)
            await self.writer.drain()

    async def client_read_loop(self):
        while 1:
            if self.stop:
                return
            chunk_b = await readpkg(self.reader)
            if chunk_b == None:
                self.writer.close()
                break
            try:
                p = self.protocol(chunk_b)
            except ProtocolError:
                self.writer.close()
                break
            self.net_queue_map[p.header.qname.decode()].put(p.body)

    async def client_loop(self):
        await asyncio.gather(
            self.client_write_loop(),
            self.client_read_loop()
        )

    def run(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop.run_until_complete(self.open_connection())
        self.loop.run_until_complete(self.client_loop())

    def get_from_net(self, queue_name):
        if isinstance(queue_name, bytes):
            queue_name = queue_name.decode()
        assert isinstance(queue_name, str), 'error queue name'
        self.data_cache.put(Protocol.build_request(Header.POP, queue_name.encode(), b''))
        if not self.net_queue_map.get(queue_name):
            self.net_queue_map[queue_name] = Queue()
        return self.net_queue_map[queue_name].get()

    def close(self):
        self.stop = True

    def __del__(self):
        self.close()
