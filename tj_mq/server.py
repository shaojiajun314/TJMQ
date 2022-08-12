import asyncio

from .utils import readpkg, ServerProtocolError
from ..abstract_server import AbstractServer
from ..protocol import ProtocolError, Protocol


class Server(AbstractServer):
    def __init__(self, port):
        super().__init__(port)

    def run(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(
            self.accept_handle,
            '0.0.0.0',
            self.port,
            loop=loop,
            # ssl=ssl_context,
        )
        server = loop.run_until_complete(coro)
        try:
            loop.run_forever()
        except Exception as e:
            print(e)
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    async def accept_handle(self, reader, writer):
        if not await self.validate_auth(reader, writer):
            writer.close()
            return
        write = self.build_write(writer)
        while True:
            try:
                chunk_b = await readpkg(reader)
            except ServerProtocolError:
                writer.close()
                return
            try:
                await self.async_protocol(chunk_b, write)
            except ProtocolError:
                writer.close()
                break

    async def validate_auth(self, reader, writer):
        auth_msg = await reader.readline()
        ret = await self.receive_auth(auth_msg)
        if ret:
            writer.write(b'ok\r\n')
        else:
            writer.write(b'no\r\n')
        return ret

    def build_write(self, writer):
        async def write(qname, msg):
            d = Protocol.build_response(qname, msg)
            writer.write(f'{len(d)}\r\n'.encode())
            writer.write(d)
            await writer.drain()
        return write
