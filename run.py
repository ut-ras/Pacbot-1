#!/usr/bin/env python3
from subprocess import Popen, PIPE, DEVNULL
from time import sleep
from algorithm import Algorithm
import traceback


def unpause():
    g.stdin.write(b'p\n')
    g.stdin.flush()


def restart():
    g.stdin.write(b'r\n')
    g.stdin.flush()


try:
    s = Popen("exec ./../Pacbot/2017-2018/gameEngine/server.py", shell=True)
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
    g.terminate()
    f.terminate()
    c.terminate()
    s.terminate()
