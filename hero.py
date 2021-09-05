# Клас для персонажа гри
class GameHero:
    def __init__(self, hight, width, x, y, speed, isJump, jumpCount):
        self.chHight = hight
        self.chWidth = width
        self.posX = x
        self.posY = y
        self.chSpeed = speed
        self.isJump = isJump
        self.jumpCount = jumpCount
        self.maxJump = 0
        self.blockSize = 0
        self.mapArr = []

    def start_pos(self, size, cubeC, map):
        self.blockSize = int(size[1]/cubeC)
        self.chHight = self.blockSize*2
        self.chWidth = self.blockSize
        self.posX = self.blockSize
        self.posY = size[1] - 3 * self.blockSize
        self.chSpeed = int(self.blockSize/10)
        self.isJump = False
        self.maxJump = int(size[1]/80)
        self.jumpCount = self.maxJump
        self.mapArr = map

    def get_pos_data(self):
        return self.posX, self.posY, self.chWidth, self.chHight

    def change_pos_x(self, val):
        if not self.collision_check(val, 0):
            self.posX += val

    def change_pos_y(self, val):
        if not self.collision_check(0, val):
            self.posY += val

    def set_jump(self, val):
        self.isJump = val

    def check_end(self, screenS):
        if self.posX < 0:
            self.posX = 0
        if self.posX + self.chWidth > screenS[0]:
            self.posX = screenS[0] - self.chWidth
        if self.posY < 0:
            self.posY = 0
        if self.posY + self.chHight > screenS[1]:
            self.posY = screenS[1] - self.chHight

    def jump_proc(self):
        if self.jumpCount >= -self.maxJump:
            if not self.collision_check(0, -int((self.jumpCount * abs(self.jumpCount)) / 2)):
                self.change_pos_y(-int((self.jumpCount * abs(self.jumpCount)) / 2))
                self.jumpCount -= 1
            else:
                if self.jumpCount >= 0:
                    self.jumpCount = -self.jumpCount
                    self.change_pos_y(int((self.jumpCount * abs(self.jumpCount)) / 2))
                    self.jumpCount -= 1
                else:
                    self.jumpCount = -self.maxJump
                    self.change_pos_y(int((self.jumpCount * abs(self.jumpCount)) / 2))
                    self.jumpCount -= 1
        else:
            self.set_jump(False)
            self.jumpCount = self.maxJump

    def collision_check(self, deltaX, deltaY):
        chX = int((self.posX + deltaX) / self.blockSize)
        chY = int((self.posY + deltaY) / self.blockSize)
        if (self.mapArr[chY][chX] == 1 or self.mapArr[chY+1][chX] == 1 or
                self.mapArr[chY][chX + 1] == 1 or self.mapArr[chY+1][chX + 1] == 1):
            return True
        return False
