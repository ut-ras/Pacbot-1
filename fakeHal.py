#!/usr/bin/env python3

from messages import pacmanState_pb2
from tcpcomms import Client


def sendPos(pos):
    msg.pacman.x = pos[0]
    msg.pacman.y = pos[1]
    client.send(msg)


client = Client(5005, pacmanState_pb2.PacmanState())
while True:
    msg = client.receive()
    sendPos((10, 15))
