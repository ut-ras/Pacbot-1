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
        if (self.gameState.mode == pacmanState_pb2.PacmanState.FRIGHTENED):
            self.FRIGHTENED = True
        else:
            self.FRIGHTENED = False
        self.betterAlgorithm()
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

    def betterAlgorithm(self):
        p_loc = (self.pacx, self.pacy)
        power_path = self.bfs(p_loc, ['o'])
        ghost_path = self.bfs(p_loc, ['G'])
        path = self.bfs(p_loc, ['.'])
        print(path)

        if ((ghost_path is not None) and self.FRIGHTENED):
            next_loc = ghost_path[1]
        elif power_path is not None:
            next_loc = power_path[1]
        elif path is not None:
            next_loc = path[1]
        else:
            next_loc = p_loc
        self.movePosition(self._get_direction(p_loc, next_loc), 1, 1)
