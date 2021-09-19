# 1 - regular block
# 2 - only top collision block
# 3 - movable block
# 4 - coin
# 5 - exit
# 6 - static enemy
# 7 - walking enemy
# 8 - flying enemy
import random


class GameMap:
    def __init__(self, x, cubeCount):
        self.extension = (x, cubeCount)
        self.mapArr = [[0] * x for i in range(cubeCount)]
        self.create_block_frame()
        self.generate_lvl()
        self.create_key()
        self.create_exit()
        self.create_st_enemy()
        self.create_mov_enemy()

    def get_map(self):
        return self.mapArr

    def create_block_frame(self):
        for i in range(len(self.mapArr)):
            for j in range(len(self.mapArr[i])):
                if i == 0 or i == self.extension[1] - 1:
                    self.mapArr[i][j] = 1
                if j == 0 or j == self.extension[0] - 1:
                    self.mapArr[i][j] = 1

    def generate_lvl(self):
        plCount = random.randint(5, 15)
        plLen = []
        plMaterial = []
        atCount = 0
        for i in range(plCount):
            plLen.append(random.randint(1, self.extension[0] - 2))
            plMaterial.append(random.randint(1, 3))
            x = 0
            y = 0
            isTake = True
            while isTake and atCount < 30:
                x = random.randint(1, self.extension[0] - 1)
                y = random.randint(1, (self.extension[1] - 1))
                if self.mapArr[y][x] == 0:
                    isTake = False
                for t in range(plLen[i]):
                    if x + t < self.extension[0] - 1 and not isTake:
                        if 1 < y + 1 < self.extension[1] and self.mapArr[y + 1][x + t] != 0:
                            isTake = True
                        if 1 < y - 1 < self.extension[1] and self.mapArr[y - 1][x + t] != 0:
                            isTake = True
                        if 1 < y + 2 < self.extension[1] and self.mapArr[y + 2][x + t] != 0:
                            isTake = True
                        if 1 < y - 2 < self.extension[1] and self.mapArr[y - 2][x + t] != 0:
                            isTake = True

                atCount += 1
            for j in range(plLen[i]):
                if 0 < x + j < self.extension[0] - 1 and 0 < y < self.extension[1] and atCount <= 30:
                    self.mapArr[y][x + j] = plMaterial[i]
        plCount = random.randint(10, 20)
        plLen = []
        plMaterial = []
        for o in range(plCount):
            plLen.append(1)
            isTake = True
            x = 0
            y = 0
            plMaterial.append(random.randint(1, 3))
            while isTake:
                x = random.randint(1, self.extension[0] - 1)
                y = random.randint(1, (self.extension[1] - 2))
                if self.mapArr[y][x] == 0:
                    isTake = False
                    if 1 < y + 1 < self.extension[1] and self.mapArr[y + 1][x] != 0:
                        isTake = True
                    if 1 < y - 1 < self.extension[1] and self.mapArr[y - 1][x] != 0:
                        isTake = True
                    if 1 < y + 2 < self.extension[1] and self.mapArr[y + 2][x] != 0:
                        isTake = True
                    if 1 < y - 2 < self.extension[1] and self.mapArr[y - 2][x] != 0:
                        isTake = True
            self.mapArr[y][x] = plMaterial[o]

    def create_st_enemy(self):
        enemyCount = random.randint(1, 5)
        for i in range(enemyCount):
            isTake = True
            x = 0
            y = 0
            while isTake:
                x = random.randint(1, self.extension[0] - 1)
                y = random.randint(1, (self.extension[1] - 2))
                if self.extension[1] > y - 1 > 0 == self.mapArr[y - 1][x] and \
                        self.extension[1] > y - 2 > 0 == self.mapArr[y - 2][x] and \
                        self.extension[1] > y + 1 > 0 != self.mapArr[y + 1][x] < 6:
                    isTake = False
            self.mapArr[y][x] = 6

    def create_mov_enemy(self):
        enemyCount = random.randint(1, 5)
        for i in range(enemyCount):
            isTake = True
            x = 0
            y = 0
            while isTake:
                x = random.randint(1, self.extension[0] - 1)
                y = random.randint(1, (self.extension[1] - 2))
                if self.mapArr[y][x] == 0 and self.extension[1] > y + 1 > 0 != self.mapArr[y + 1][x] < 6:
                    isTake = False
            self.mapArr[y][x] = 7
        enemyCount = random.randint(1, 5)
        for i in range(enemyCount):
            isTake = True
            x = 0
            y = 0
            while isTake:
                x = random.randint(1, self.extension[0] - 1)
                y = random.randint(1, (self.extension[1] - 2))
                if self.mapArr[y][x] == 0 and self.extension[0] > x + 1 > 0 == self.mapArr[y][x + 1]:
                    isTake = False
            self.mapArr[y][x] = 8

    def create_key(self):
        keyAmount = random.randint(3, 5)
        for i in range(keyAmount):
            isTake = True
            x = 0
            y = 0
            while isTake:
                x = random.randint(1, self.extension[0] - 1)
                y = random.randint(1, (self.extension[1] - 2))
                if self.mapArr[y][x] == 0:
                    if self.extension[1] > y - 1 > 0 == self.mapArr[y - 1][x] and \
                            self.extension[1] > y - 2 > 0 == self.mapArr[y - 2][x]:
                        isTake = False
                    if self.extension[1] > y - 1 > 0 == self.mapArr[y - 1][x] and \
                            self.extension[1] > y + 1 > 0 and 2 == self.mapArr[y + 1][x]:
                        isTake = False
            self.mapArr[y][x] = 4

    def create_exit(self):
        isTake = True
        x = 0
        y = 0
        while isTake:
            x = random.randint(1, self.extension[0] - 1)
            y = random.randint(1, (self.extension[1] - 2))
            if self.mapArr[y][x] == 0 and self.extension[1] > y + 1 > 0 == self.mapArr[y + 1][x] and \
                    self.extension[1] > y + 2 > 0 != self.mapArr[y + 2][x]:
                isTake = False
        self.mapArr[y][x] = 5
        self.mapArr[y+1][x] = 5

