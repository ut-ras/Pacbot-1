#!/usr/bin/env python3

import pickle
from time import sleep

from messages import hardware_pb2
from tcpcomms import Client

DELAY = 0


def delay():
    sleep(DELAY)


def invalid(x, y):
    if (grid[x][y] in ['G', '#']):
        print("invalid")
        return True
    elif hardware.move == hardware_pb2.Move.UNTIL and hardware.moveuntil.stop:
        print("invalid")
        return True
    return False


def movePosition(currentPos, direction, distance):
    x, y = currentPos
    if (distance > 0):
        if (direction == hardware_pb2.Move.Direction.Value('UP')):
            for i in range(0, distance):
                hardware.currentPos.x -= 1
                delay()
        elif (direction == hardware_pb2.Move.Direction.Value('DOWN')):
            for i in range(0, distance):
                hardware.currentPos.x += 1
                delay()
        elif (direction == hardware_pb2.Move.Direction.Value('RIGHT')):
            for i in range(0, distance):
                hardware.currentPos.y += 1
                delay()
        elif (direction == hardware_pb2.Move.Direction.Value('LEFT')):
            for i in range(0, distance):
                hardware.currentPos.y -= 1
                delay()


def moveUntil(currentPos, direction):
    x, y = currentPos
    if (direction != hardware_pb2.Move.Direction.Value('NONE')):
        hardware.orientation = direction
        delay()
    if (direction == hardware_pb2.Move.Direction.Value('LEFT')):
        if (invalid(hardware.currentPos.x - 1, hardware.currentPos.y)):
            return
        hardware.currentPos.x -= 1
        delay()
    elif (direction == hardware_pb2.Move.Direction.Value('RIGHT')):
        if (invalid(hardware.currentPos.x + 1, hardware.currentPos.y)):
            return
        hardware.currentPos.x += 1
        delay()
    elif (direction == hardware_pb2.Move.Direction.Value('UP')):
        if (invalid(hardware.currentPos.x, hardware.currentPos.y + 1)):
            return
        hardware.currentPos.y += 1
        delay()
    elif (direction == hardware_pb2.Move.Direction.Value('DOWN')):
        if (invalid(hardware.currentPos.x, hardware.currentPos.y - 1)):
            return
        hardware.currentPos.y -= 1
        delay()


client = Client(5006, hardware_pb2.Move())
print("fakehal connected")
sleep(1)
with open('grid.pkl', 'rb') as f:
    grid = pickle.load(f)
while True:
    hardware = client.receive()
    if hardware.move == hardware_pb2.Move.POSITION:
        movePosition((hardware.currentPos.x, hardware.currentPos.y),
                     hardware.moveposition.direction,
                     hardware.moveposition.distance)
    elif hardware.move == hardware_pb2.Move.UNTIL:
        moveUntil((hardware.currentPos.x, hardware.currentPos.y),
                  hardware.moveuntil.direction)
    client.send(hardware)
