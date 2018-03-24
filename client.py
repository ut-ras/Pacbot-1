#!/usr/bin/env python3

import socket
import os
from messages.subscribe_pb2 import Subscribe
from messages.lightState_pb2 import LightState
from messages import MsgType
import struct
from messages import pacmanState_pb2
from tcpcomms import Server

_SUBSCRIBE = 15000
MAGIC_HEADER = 17380
SIZE_HEADER = struct.Struct("!HHH")


def pack_msg(msg, msg_type):
    if msg_type == _SUBSCRIBE:
        header = SIZE_HEADER.pack(MAGIC_HEADER, msg_type, len(msg))
    else:
        header = SIZE_HEADER.pack(MAGIC_HEADER, msg_type.value, len(msg))
    return header + msg


def subscribe():
    msg = Subscribe()
    # In production we'll use FULL_STATE for pellet locations, frightened timer,
    # and ghost directions. LIGHT_STATE is just for testing since it's
    # readable.
    msg.msg_types.append(MsgType.FULL_STATE.value)
    msg.dir = 0
    s.send(pack_msg(msg.SerializeToString(), _SUBSCRIBE))


def broadcastPos(pos):
    msg = LightState.AgentState()
    msg.x = pos[0]
    msg.y = pos[1]
    s.send(pack_msg(msg.SerializeToString(), MsgType.PACMAN_LOCATION))


def msg_received(data, msg_type):
    msg = pacmanState_pb2.PacmanState()
    msg.ParseFromString(data)
    return msg


HOST = os.environ.get("LOCAL_ADDRESS", "localhost")
PORT = os.environ.get("BIND_PORT", 11297)
addr = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(addr)
subscribe()

server = Server(5005, pacmanState_pb2.PacmanState())

while True:
    data = s.recv(2048)
    magic, msg_type, length = SIZE_HEADER.unpack(data[:SIZE_HEADER.size])
    buf = data[SIZE_HEADER.size:]
    if msg_type == MsgType.FULL_STATE.value:
        message = msg_received(buf[:length], msg_type)
        server.send(message)
        rec = server.receive()
        broadcastPos((rec.pacman.x, rec.pacman.y))
        #x, y = map(int, raw_input("Input a new x y position for pacman: ").split())
        #broadcastPos((x, y))
