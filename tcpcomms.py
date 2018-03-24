from struct import pack, unpack
import socket


class TCPProto:
    def __init__(self, port):
        self.host = '127.0.0.1'
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.sock.close()


class Server(TCPProto):
    # port is tcp port, proto is base protobuf message ex. ***_pb2.Message()
    def __init__(self, port, proto):
        super(Server, self).__init__(port)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        self.proto = proto

    def send(self, message):
        encoded = message.SerializeToString()
        header = pack('I', len(encoded))
        self.conn.sendall(header)
        self.conn.sendall(encoded)

    def receive(self):
        length, = unpack('I', self.conn.recv(4))
        self.proto.ParseFromString(self.conn.recv(length))
        return self.proto


class Client(TCPProto):
    # port is tcp port, proto is base protobuf message ex. ***_pb2.Message()
    def __init__(self, port, proto):
        super(Client, self).__init__(port)
        self.proto = proto
        self.sock.connect((self.host, self.port))

    def send(self, message):
        encoded = message.SerializeToString()
        header = pack('I', len(encoded))
        self.sock.sendall(header)
        self.sock.sendall(encoded)

    def receive(self):
        length, = unpack('I', self.sock.recv(4))
        self.proto.ParseFromString(self.sock.recv(length))
        return self.proto
