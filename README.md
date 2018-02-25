# Pacbot-1

First clone and run the pacbot server and communications scripts
```
git clone https://github.com/HarvardURC/Pacbot.git
cd Pacbot/2017-2018/gameEngine
./server.py
./gameEngine.py
cd ../botCode
./server.py
./pacbotCommsModule.py
```

then clone this repo, build the protobufs and run the script
```
git clone https://github.com/ut-ras/Pacbot-1.git
cd Pacbot-1
make protobuf
python3 client.py
```
