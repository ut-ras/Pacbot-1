import socket
import os
from messages.subscribe_pb2 import Subscribe
from messages import MsgType
from messages import message_buffers
from constants import _SUBSCRIBE, MAGIC_HEADER, SIZE_HEADER


def pack_msg(msg, msg_type):
    if msg_type == _SUBSCRIBE:
        header = SIZE_HEADER.pack(MAGIC_HEADER, msg_type, len(msg))
    else:
        header = SIZE_HEADER.pack(MAGIC_HEADER, msg_type.value, len(msg))
    return header + msg


def subscribe(msg_types, direction):
        msg = Subscribe()
        '''
        for msg_type in msg_types:
            msg.msg_types.append(msg_type.value)
        '''
        msg.msg_types.append(MsgType.LIGHT_STATE.value)
        msg.msg_types.append(MsgType.PACMAN_LOCATION.value)
        msg.dir = direction
        s.send(pack_msg(msg.SerializeToString(), _SUBSCRIBE))


def msg_received(data, msg_type):
        if msg_type != _SUBSCRIBE:
            msg = message_buffers[MsgType(msg_type)]()
            msg.ParseFromString(data)
            # msg access syntax is in samplePacbotModule
            print(msg)


HOST = os.environ.get("LOCAL_ADDRESS", "localhost")
PORT = os.environ.get("BIND_PORT", 11297)

addr = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(addr)
print("connected")
subscribe(MsgType, Subscribe.SUBSCRIBE)
while True:
    data = s.recv(2048)
    magic, msg_type, length = SIZE_HEADER.unpack(
                        data[:SIZE_HEADER.size])
    buf = data[SIZE_HEADER.size:]
    msg_received(buf[:length], msg_type)
