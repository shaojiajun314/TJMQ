class ProtocolError(Exception):
    pass


class Header():
    SPLIT = '$_$'.encode()
    PUSH = 'PUSH'.encode()
    POP = 'POP'.encode()
    RESPONSE = 'RESPONSE'.encode()
    METHODS = (PUSH, POP, RESPONSE)
    def __init__(self, header_frame):
        self.qname = None
        self.method = None
        self.parse_header(header_frame)

    def parse_header(self, header_frame):
        try:
            method, qname = header_frame.split(self.SPLIT, 1)
            assert method in self.METHODS, f'error method: {method}'
        except:
            raise ProtocolError()
        self.qname = qname
        self.method = method


class Protocol():
    SPLIT = '(￣﹁￣)'.encode()
    def __init__(self, frame):
        self.frame = frame
        self.header = None
        self.body = None
        self.parser_frame()

    def parser_frame(self):
        try:
            header, body = self.frame.split(self.SPLIT, 1)
            header = bytes.fromhex(header.decode())
            self.header = Header(header)
            self.body = body
        except:
            raise ProtocolError()

    @classmethod
    def build_request(cls, method, q_name, body):
        return cls.SPLIT.join(
            (
                Header.SPLIT.join((method, q_name)).hex().encode(),
                body
            )
        )

    @classmethod
    def build_response(cls, q_name, body):
        return cls.SPLIT.join(
            (
                Header.SPLIT.join((Header.RESPONSE, q_name)).hex().encode(),
                body
            )
        )
