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
        self.algorithm()
        print(self)
        self.server.send(self.hardware)
        self.hardware = self.server.receive()
        self.gameState.pacman.x = self.hardware.currentPos.x
        self.gameState.pacman.y = self.hardware.currentPos.y
        self.client.send(self.gameState)

    def algorithm(self):
        self.directionTaken = '(' + str(self.pacx) + ',' + str(self.pacy) + ')'
        pellet = ['.', 'o']
        if (self.grid[self.pacx][self.pacy - 1] in pellet):
            self.movePosition('LEFT', 1, 0)
            self.directionTaken += 'LEFT'
        elif (self.grid[self.pacx][self.pacy + 1] in pellet):
            self.movePosition('RIGHT', 1, 0)
            self.directionTaken += 'RIGHT'
        elif (self.grid[self.pacx + 1][self.pacy] in pellet):
            self.movePosition('DOWN', 1, 0)
            self.directionTaken += 'DOWN'
        elif (self.grid[self.pacx - 1][self.pacy] in pellet):
            self.movePosition('UP', 1, 0)
            self.directionTaken += 'UP'
        elif (self.grid[self.pacx][self.pacy - 1] == ' '):
            self.movePosition('LEFT', 1, 0)
            self.directionTaken += 'LEFT'
        elif (self.grid[self.pacx][self.pacy + 1] == ' '):
            self.movePosition('RIGHT', 1, 0)
            self.directionTaken += 'RIGHT'
        elif (self.grid[self.pacx + 1][self.pacy] == ' '):
            self.movePosition('DOWN', 1, 0)
            self.directionTaken += 'DOWN'
        elif (self.grid[self.pacx - 1][self.pacy] == ' '):
            self.movePosition('UP', 1, 0)
            self.directionTaken += 'UP'
