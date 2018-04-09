from messages import pacmanState_pb2, hardware_pb2
from tcpcomms import Client, Server


class AlgorithmBase:
    def __init__(self):
        self.client = Client(5005, pacmanState_pb2.PacmanState())
        self.server = Server(5006, hardware_pb2.Move())
        print("algorithm server")
        self.gameState = pacmanState_pb2.PacmanState()
        self.hardware = hardware_pb2.Move()
        self.PAUSED = False
        self.grid = []
        self.score = 0
        self.lives = 3
        ## DEBUG
        self.directionTaken = 'NONE'

    def updateGrid(self):
        self.pacx = self.gameState.pacman.x
        self.pacy = self.gameState.pacman.y
        self.lives = self.gameState.lives
        self.score = self.gameState.score
        self.grid = []
        row_index = 0
        col_index = 0
        row = []
        ghosts = [(self.gameState.red_ghost.x, self.gameState.red_ghost.y),
                  (self.gameState.orange_ghost.x,
                   self.gameState.orange_ghost.y),
                  (self.gameState.pink_ghost.x,
                   self.gameState.pink_ghost.y), (self.gameState.blue_ghost.x,
                                                  self.gameState.blue_ghost.y)]
        for el in self.gameState.grid:
            if (col_index, row_index) == (self.gameState.pacman.x,
                                          self.gameState.pacman.y):
                row.append('P')
            elif (col_index, row_index) in ghosts:
                row.append('G')
            elif el == pacmanState_pb2.PacmanState.PELLET:
                row.append('.')
            elif el == pacmanState_pb2.PacmanState.POWER_PELLET:
                row.append('o')
            elif el == pacmanState_pb2.PacmanState.EMPTY:
                row.append(' ')
            elif el == pacmanState_pb2.PacmanState.WALL:
                row.append('#')
            row_index += 1
            if row_index >= self.gameState.grid_columns:
                row_index = 0
                col_index += 1
                self.grid.append(row)
                row = []

    def simInit(self):
        self.gameState = self.client.receive()
        self.updateGrid()
        self.client.send(self.gameState)

    def movePosition(self, direction, distance, speed, orientation='NONE'):
        self.hardware.currentPos.x = self.gameState.pacman.x
        self.hardware.currentPos.y = self.gameState.pacman.y
        self.hardware.move = hardware_pb2.Move.POSITION
        self.hardware.speed = speed
        self.hardware.moveposition.distance = distance
        self.hardware.moveposition.direction = hardware_pb2.Move.Direction.Value(
            direction)

    def moveUntil(self, direction, speed, orientation='NONE'):
        self.hardware.currentPos.x = self.gameState.pacman.x
        self.hardware.currentPos.y = self.gameState.pacman.y
        self.hardware.move = hardware_pb2.Move.UNTIL
        self.hardware.moveposition.direction = hardware_pb2.Move.Direction.Value(
            direction)

    def __str__(self):
        out = ''
        for row in self.grid:
            out += ''.join(row)
            out += '\n'
        out += '\nScore: ' + str(self.score) + '\nLives: ' + str(
            self.lives) + '\n'
        out += 'direction taken: ' + self.directionTaken + '\n'
        return out
