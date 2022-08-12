import asyncio
from pickle import loads as p_loads

from .protocol import Protocol, Header
from TJQueue.queue import get_queue


class AbstractServer():
    def __init__(self, port):
        self.port = port
        self.loop = asyncio.get_event_loop()

    def protocol(self, msg, write=None):
        p = Protocol(msg)
        q = get_queue(p.header.qname)
        if p.header.method == Header.PUSH:
            q.push(p.body)
        elif p.header.method == Header.POP:
            write(p.header.qname, q.pop())

    async def async_protocol(self, msg, write=None):
        p = Protocol(msg)
        q = get_queue(p.header.qname)
        print('receive request: ', p.header.method, p.header.qname)
        if p.header.method == Header.PUSH:
            await self.loop.run_in_executor(None, q.push, p.body)
        elif p.header.method == Header.POP:
            await write(
                p.header.qname,
                await self.loop.run_in_executor(None, q.pop)
            )

    async def receive_auth(self, msg):
        msg = p_loads(bytes.fromhex(msg.decode()))
        print(f'receive auth msg: {msg}')
        return True

    def run(self):
        raise NotImplementedError()

    def close(self, queue):
        get_queue(queue).close()
