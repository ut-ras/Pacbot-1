#!/usr/bin/env python3
import sys
import traceback
from subprocess import DEVNULL, PIPE, Popen
from time import sleep

from algorithm import Algorithm
from messages import gameMode_pb2
from tcpcomms import Client, Server

runMode = 0


def unpause():
    g.stdin.write(b'p\n')
    g.stdin.flush()


def bot_unpause():
    mode.PAUSED = True
    modeClient.send(mode)


def restart():
    g.stdin.write(b'r\n')
    g.stdin.flush()


try:
    if(len(sys.argv) > 1):
        if(sys.argv[1] == 'server'):
            runMode = 1
            s = Popen(
                "exec ./../Pacbot/2017-2018/gameEngine/server.py", shell=True)
            print("server started")
            g = Popen(
                "exec ./../Pacbot/2017-2018/gameEngine/gameEngine.py",
                stdout=DEVNULL,
                stdin=PIPE,
                shell=True)
            print("gameEngine started")
            modeServer = Server(5007, gameMode_pb2.Pause())
            count = 0
            while(True):
                mode = modeServer.receive()
                if(count == 2 and mode.PAUSED):
                    restart()
                    count = 0
                elif(mode.PAUSED):
                    unpause()
                    count += 1
        elif(sys.argv[1] == 'bot'):
            runMode = 2
            c = Popen('exec ./client.py', shell=True)
            sleep(1)
            f = Popen('exec ./fakehal.py', shell=True)
            simulation = Algorithm()
            print("simulation")
            modeClient = Client(5007, gameMode_pb2.Pause())
            mode = gameMode_pb2.Pause()
            sleep(0.5)
            count = 0
            bot_unpause()
            sleep(1)
            simulation.simInit()
            while True:
                simulation.tick()
                if (simulation.PAUSED is True):
                    if (simulation.lives) == 1:
                        print('Score: ' + str(simulation.score))
                        if (count == 1):
                            restart()
                            simulation.simInit()
                        count += 1
                    print('Score: ' + str(simulation.score) + ', lives: ' +
                          str(simulation.lives))
                    bot_unpause()
                    simulation.simInit()
                    simulation.PAUSED = False
        elif (sys.argv[1] == 'competition'):
            runMode = 2
            c = Popen('exec ./client.py', shell=True)
            sleep(1)
            f = Popen('exec ./fakehal.py', shell=True)
            simulation = Algorithm()
            print("competition")
            sleep(1.5)
            simulation.compInit()
            while True:
                simulation.competition_tick()
                if (simulation.PAUSED is True):
                    while(simulation.update_pause()):
                        sleep(0.5)
                    simulation.compInit()
                    simulation.PAUSED = False
    else:
        s = Popen(
            "exec ./../Pacbot/2017-2018/gameEngine/server.py", shell=True)
        print("server started")
        g = Popen(
            "exec ./../Pacbot/2017-2018/gameEngine/gameEngine.py",
            stdout=DEVNULL,
            stdin=PIPE,
            shell=True)
        print("gameEngine started")
        unpause()
        sleep(0.5)
        c = Popen('exec ./client.py', shell=True)
        sleep(1)
        f = Popen('exec ./fakehal.py', shell=True)
        simulation = Algorithm()
        print("simulation")
        sleep(0.5)
        count = 0
        simulation.simInit()
        while True:
            simulation.tick()
            if (simulation.PAUSED is True):
                if (simulation.lives) == 1:
                    print('Score: ' + str(simulation.score))
                    if (count == 1):
                        restart()
                        simulation.simInit()
                    count += 1
                print('Score: ' + str(simulation.score) + ', lives: ' +
                      str(simulation.lives))
                unpause()
                simulation.simInit()
                simulation.PAUSED = False

except Exception:
    print("\nQuitting\n")
    traceback.print_exc()
    if runMode in [0, 1]:
        g.terminate()
    if runMode in [0, 2]:
        f.terminate()
    if runMode in [0, 2]:
        c.terminate()
    if runMode in [0, 1]:
        s.terminate()
