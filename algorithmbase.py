import copy
import pickle

from messages import hardware_pb2, pacmanState_pb2
from tcpcomms import Client, Server


class AlgorithmBase:
    def __init__(self):
        self.client = Client(5005, pacmanState_pb2.PacmanState())
        self.server = Server(5006, hardware_pb2.Move())
        print("algorithm server")
        self.gameState = pacmanState_pb2.PacmanState()
        self.hardware = hardware_pb2.Move()
        self.PAUSED = True
        self.FRIGHTENED = False
        self.grid = []
        self.score = 0
        self.lives = 3
        # DEBUG
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
        """
        movable = ['.', ' ']
        for i in range(1, len(self.grid) - 1):
            for j in range(1, len(self.grid[i]) - 1):
                if(self.grid[i][j] in movable and self.grid[i - 1][j] in movable and self.grid[i + 1][j] in movable and self.grid[i][j - 1] in movable and self.grid[i][j + 1] in movable):
                    self.grid[i][j] = '#'
        """

    def simInit(self):
        self.gameState = self.client.receive()
        self.updateGrid()
        with open('grid.pkl', 'wb') as f:
            pickle.dump(self.grid, f)
        self.client.send(self.gameState)

    def compInit(self):
        self.gameState = self.client.receive()
        self.updateGrid()

    def update_pause(self):
        self.gameState = self.client.receive()
        if (self.gameState.mode == pacmanState_pb2.PacmanState.PAUSED):
            self.PAUSED = True
        else:
            self.PAUSED = False
        return self.PAUSED

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
        self.hardware.speed = speed
        self.hardware.moveuntil.direction = hardware_pb2.Move.Direction.Value(
            direction)

    def noGhost(self, path):
        for coord in path:
            if(self.grid[coord[0]][coord[1]] == 'G'):
                return False
        return True

    def bfs(self, start, target, max_dist=float("inf")):
        visited = []
        queue = [(start, [])]

        while len(queue) > 0:
            nxt = queue.pop(0)
            visited.append(nxt[0])
            new_path = copy.deepcopy(nxt[1])
            new_path.append(nxt[0])
            loc = nxt[0]
            if type(target) is tuple:
                if target == loc:
                    return new_path
            elif self.grid[loc[0]][loc[1]] in target:
                if(self.FRIGHTENED):
                    return new_path
                elif(self.noGhost(new_path)):
                    return new_path

            if self.grid[loc[0] + 1][loc[1]] in [
                    '.', 'o', ' ', 'G'
            ] and (loc[0] + 1,
                   loc[1]) not in visited and len(new_path) <= max_dist:
                queue.append(((loc[0] + 1, loc[1]), new_path))
            if self.grid[loc[0] - 1][loc[1]] in [
                    '.', 'o', ' ', 'G'
            ] and (loc[0] - 1,
                   loc[1]) not in visited and len(new_path) <= max_dist:
                queue.append(((loc[0] - 1, loc[1]), new_path))
            if self.grid[loc[0]][loc[1] + 1] in [
                    '.', 'o', ' ', 'G'
            ] and (loc[0],
                   loc[1] + 1) not in visited and len(new_path) <= max_dist:
                queue.append(((loc[0], loc[1] + 1), new_path))
            if self.grid[loc[0]][loc[1] - 1] in [
                    '.', 'o', ' ', 'G'
            ] and (loc[0],
                   loc[1] - 1) not in visited and len(new_path) <= max_dist:
                queue.append(((loc[0], loc[1] - 1), new_path))

        return None

    def _get_direction(self, p_loc, next_loc):
        if p_loc[0] == next_loc[0]:
            if p_loc[1] < next_loc[1]:
                return "UP"
            else:
                return "DOWN"
        else:
            if p_loc[0] < next_loc[0]:
                return "RIGHT"
            else:
                return "LEFT"

    def __str__(self):
        out = ''
        for row in self.grid:
            out += ''.join(row)
            out += '\n'
        out += '\nScore: ' + str(self.score) + '\nLives: ' + str(
            self.lives) + '\n'
        out += 'FRIGHTENED: ' + str(self.FRIGHTENED) + '\n'
        return out
