class ServerProtocolError(Exception):
    pass


async def readpkg(reader):
    try:
        chunk_h = (await reader.readline()).decode()
        size = int(chunk_h.strip())
    except Exception as e:
        print(e, 'error')
        raise ServerProtocolError()
    chunk_b = await reader.read(size)
    return chunk_b
