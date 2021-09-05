
class GameMap:
    def __init__(self, x, cubeCount):
        self.extension = (x, cubeCount)
        self.mapArr = [[0] * x for i in range(cubeCount)]
        self.create_block_frame()

    def get_map(self):
        return self.mapArr

    def create_block_frame(self):
        for i in range(len(self.mapArr)):
            for j in range(len(self.mapArr[i])):
                if i == 0 or i == self.extension[1] - 1:
                    self.mapArr[i][j] = 1
                if j == 0 or j == self.extension[0] - 1:
                    self.mapArr[i][j] = 1

