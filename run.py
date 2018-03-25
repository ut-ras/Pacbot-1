#!/usr/bin/env python3
from subprocess import Popen, PIPE, DEVNULL
from time import sleep

try:
    s = Popen("exec ./../Pacbot/2017-2018/gameEngine/server.py", shell=True)
    print("server started")
    g = Popen(
        "exec ./../Pacbot/2017-2018/gameEngine/gameEngine.py",
        stdout=DEVNULL,
        stdin=PIPE,
        shell=True)
    print("gameEngine started")
    g.stdin.write(b'p\n')
    g.stdin.flush()
    sleep(0.1)
    c = Popen('exec ./client.py', shell=True)
    sleep(0.1)
    f = Popen('exec ./fakeHal.py', shell=True)
    while True:
        sleep(5)
except KeyboardInterrupt:
    print("Quitting")
    f.terminate()
    c.terminate()
    s.terminate()
    g.terminate()
