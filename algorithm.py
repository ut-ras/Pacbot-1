from algorithmbase import AlgorithmBase
from messages import pacmanState_pb2


class Algorithm(AlgorithmBase):
    def __init__(self):
        super(Algorithm, self).__init__()

    def tick(self):
        self.gameState = self.client.receive()
        self.updateGrid()
        if (self.gameState.mode == pacmanState_pb2.PacmanState.PAUSED):
            self.PAUSED = True
        else:
            self.PAUSED = False
        self.basicAlgorithm()
        print(self)
        self.server.send(self.hardware)
        self.hardware = self.server.receive()
        self.gameState.pacman.x = self.hardware.currentPos.x
        self.gameState.pacman.y = self.hardware.currentPos.y
        self.client.send(self.gameState)

    def basicAlgorithm(self):
        p_loc = (self.pacx, self.pacy)
        path = self.bfs(p_loc, ['o'])
        print(path)

        if path is not None:
            next_loc = path[1]
            self.movePosition(self._get_direction(p_loc, next_loc), 1, 1)
