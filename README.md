# pb-Buster

First clone the Harvard Pacbot Repo
```
git clone https://github.com/HarvardURC/Pacbot.git
```
* In `Pacbot/2017-2018/gameEngine/pacbot/variables.py` change the `game_frequency` value to `4` or `5` to speed up the game

then clone this repo alongside Harvard's repo, build the protobufs and run the simulation
```
git clone https://github.com/ut-ras/pb-Buster.git
cd  pb-Buster
make protobuf
./run.py
```
