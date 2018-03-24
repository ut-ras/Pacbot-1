#!/usr/bin/env python3

from messages import lightState_pb2
from tcpcomms import Client


def sendPos(pos):
    msg.pacman.x = pos[0]
    msg.pacman.y = pos[1]
    client.send(msg)


client = Client(5005, lightState_pb2.LightState())
while True:
    msg = client.receive()
    sendPos((10, 15))
