#!/usr/bin/env python3

from messages import hardware_pb2
from tcpcomms import Client
from time import sleep

DELAY = 0


def delay():
    sleep(DELAY)


def inValid(x, y):
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
    if (direction != hardware_pb2.Direction.NONE):
        hardware.orientation = direction
        delay()
    if (direction == hardware_pb2.Direction.WEST):
        while True:
            if (inValid(hardware.currentPos.x - 1, hardware.currentPos.y)):
                break
            hardware.currentPos.x -= 1
            delay()
    elif (direction == hardware_pb2.Direction.EAST):
        while True:
            if (inValid(hardware.currentPos.x + 1, hardware.currentPos.y)):
                break
            hardware.currentPos.x += 1
            delay()
    elif (direction == hardware_pb2.Direction.NORTH):
        while True:
            if (inValid(hardware.currentPos.x, hardware.currentPos.y + 1)):
                break
            hardware.currentPos.y += 1
            delay()
    elif (direction == hardware_pb2.Direction.SOUTH):
        while True:
            if (inValid(hardware.currentPos.x, hardware.currentPos.y - 1)):
                break
            hardware.currentPos.y -= 1
            delay()


client = Client(5006, hardware_pb2.Move())
print("fakehal connected")
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
