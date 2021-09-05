# Клас для персонажа гри
import pygame


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
        self.chObj = pygame.Rect(0, 0, 0, 0)
        self.chImg = {}
        self.collision = []
        self.collisionTypes = {}

    def start_pos(self, size, cubeC, map, win):
        self.blockSize = int(size[1]/cubeC)
        self.chHight = self.blockSize*2
        self.chWidth = self.blockSize
        self.posX = int(self.blockSize) + 10
        self.posY = int(size[1] - 3 * self.blockSize) - 10
        self.chSpeed = int(self.blockSize/5)
        self.isJump = False
        self.maxJump = int(size[1]/80)
        self.jumpCount = self.maxJump
        self.mapArr = map
        self.chObj = pygame.Rect(self.posX, self.posY, self.chWidth, self.chHight)
        self.chImg = pygame.image.load("b.png")
        self.collisionTypes = {'top': False, 'right': False, 'bottom': False, 'left': False}

    def draw_ch(self, win):
        self.chObj = pygame.Rect(self.chObj.x, self.chObj.y, self.chWidth, self.chHight)

    def change_pos_x(self, val, allBlock):
        if len(self.collision_check(allBlock)) == 0:
            self.posX = int(self.posX + val)

    def change_pos_y(self, val, allBlock):
        if len(self.collision_check(allBlock)) == 0:
            self.posY = int(self.posY + val)

    def set_pos_x(self, val):
        self.posX = int(val)

    def set_pos_y(self, val):
        self.posY = int(val)

    def set_jump(self, val):
        self.isJump = val

    def collision_check(self, allBlock):
        self.collision = []
        for block in allBlock:
            if self.chObj.colliderect(block):
                self.collision.append(block)
        return self.collision

    def type_of_collision(self, allBlock, deltaX, deltaY):
        self.collisionTypes = {'top': False, 'right': False, 'bottom': False, 'left': False}
        print(self.chObj.x, self.chObj.y, " - 1")
        self.chObj.x += deltaX
        self.collision = self.collision_check(allBlock)
        for block in self.collision:
            if deltaX > 0:
                self.chObj.right = block.left
                self.collisionTypes['right'] = True
            elif deltaX < 0:
                self.chObj.left = block.right
                self.collisionTypes['left'] = True
        self.chObj.y += deltaY
        self.collision = self.collision_check(allBlock)
        for block in self.collision:
            if deltaY > 0:
                self.chObj.bottom = block.top
                self.collisionTypes['bottom'] = True
            elif deltaY < 0:
                self.chObj.top = block.bottom
                self.collisionTypes['top'] = True
        print(self.chObj.x, self.chObj.y, " - 2")

    def do_jump(self, allBlock):
        if self.jumpCount >= -self.maxJump:
            if len(self.collision_check(allBlock)) == 0:
                self.change_pos_y(-int((self.jumpCount * abs(self.jumpCount)) / 2), allBlock)
                self.jumpCount -= 1
            else:
                if self.jumpCount >= 0:
                    self.jumpCount = -self.jumpCount
                    # self.change_pos_y(int((self.jumpCount * abs(self.jumpCount)) / 2))
                    self.jumpCount -= 1
                else:
                    self.jumpCount = -self.maxJump
                    # self.change_pos_y(int((self.jumpCount * abs(self.jumpCount)) / 2))
                    self.jumpCount -= 1
        else:
            self.set_jump(False)
            self.jumpCount = self.maxJump
