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
        self.allBlockSt = []
        self.chObj = pygame.Rect(0, 0, 0, 0)
        self.chImg = {}
        self.collision = []
        self.collisionTypes = {}
        self.keyCount = 0
        self.inAir = True
        self.isUp = False
        self.isDown = False
        self.isEnd = False
        self.life = 3
        self.timePoint = 100000

    def start_pos(self, size, cubeC, map, allBlockSt):
        self.isUp = False
        self.blockSize = int(size[1]/cubeC)
        self.chHight = int(self.blockSize * 1.9)
        self.chWidth = int(self.blockSize * 0.9)
        self.posX = int(self.blockSize) + 10
        self.posY = int(size[1] - 3 * self.blockSize) - 10
        self.chSpeed = int(self.blockSize/3)
        self.isJump = False
        self.maxJump = int(size[1]/75)
        self.jumpCount = self.maxJump
        self.mapArr = map
        self.chObj = pygame.Rect(self.posX, self.posY, self.chWidth, self.chHight)
        self.chImg = pygame.image.load("b.png")
        self.collisionTypes = {'top': False, 'right': False, 'bottom': False, 'left': False}
        self.keyCount = 0
        self.allBlockSt = allBlockSt
        self.isEnd = False

    def set_pos_x(self, val):
        self.posX = int(val)

    def set_pos_y(self, val):
        self.posY = int(val)

    def set_jump(self, val):
        self.isJump = val

    def collision_check(self, allBlock, x, y):
        self.collision = []
        for block in allBlock:
            blockMaterial = self.mapArr[int(block.y / self.blockSize)][int(block.x / self.blockSize)]
            if blockMaterial == 2:
                if self.chObj.colliderect(block):
                    if self.isDown and self.chObj.y + self.chHight - y <= block.y:
                        self.collision.append(block)
                    elif not self.isDown and not self.isUp and self.chObj.y + self.chHight - y <= block.y:
                        self.collision.append(block)
            elif self.chObj.colliderect(block):
                self.collision.append(block)
        return self.collision

    def type_of_collision(self, allBlock, deltaX, deltaY):
        self.collisionTypes = {'top': False, 'right': False, 'bottom': False, 'left': False}
        self.chObj.x += deltaX
        self.collision = self.collision_check(allBlock, deltaX, deltaY)
        for block in self.collision:
            blockMaterial = self.mapArr[int(block.y/self.blockSize)][int(block.x/self.blockSize)]
            if blockMaterial == 1 or blockMaterial == 3:
                if deltaX > 0:
                    self.chObj.right = block.left
                    self.collisionTypes['right'] = True
                elif deltaX < 0:
                    self.chObj.left = block.right
                    self.collisionTypes['left'] = True
        self.chObj.y += deltaY
        self.collision = self.collision_check(allBlock, deltaX, deltaY)
        for block in self.collision:
            y = int(block.y/self.blockSize)
            x = int(block.x/self.blockSize)
            blockMaterial = self.mapArr[y][x]
            if blockMaterial == 1:
                if deltaY > 0:
                    self.chObj.bottom = block.top
                    self.collisionTypes['bottom'] = True
                    self.inAir = False
                    self.isUp = self.isDown = False
                elif deltaY < 0:
                    self.chObj.top = block.bottom
                    self.collisionTypes['top'] = True
                    self.isUp = self.isDown = False
            elif blockMaterial == 2:
                if deltaY > 0:
                    self.chObj.bottom = block.top
                    self.collisionTypes['bottom'] = True
                    self.inAir = False
                    self.isUp = self.isDown = False
            elif blockMaterial == 3:
                if deltaY > 0:
                    self.chObj.bottom = block.top
                    self.collisionTypes['bottom'] = True
                    self.inAir = False
                    self.isUp = self.isDown = False
                    if self.allBlockSt[y][x] > 0:
                        self.allBlockSt[y][x] -= 1
                    else:
                        self.mapArr[y][x] = 0
                elif deltaY < 0:
                    self.chObj.top = block.bottom
                    self.collisionTypes['top'] = True
                    self.isUp = self.isDown = False
        self.collision = self.collision_check(allBlock, deltaX, deltaY)
        for block in self.collision:
            y = int(block.y/self.blockSize)
            x = int(block.x/self.blockSize)
            blockMaterial = self.mapArr[y][x]
            if blockMaterial == 4:
                self.keyCount += 1
                self.mapArr[y][x] = 0
            if blockMaterial == 5 and self.keyCount == 5:
                self.isEnd = True

        return self.mapArr

    def do_jump(self, allBlock):
        if self.jumpCount >= -self.maxJump:
            if (self.jumpCount * abs(self.jumpCount)) < 0:
                self.isDown = True
                self.isUp = False
            elif (self.jumpCount * abs(self.jumpCount)) > 0:
                self.isUp = True
                self.isDown = False
            else:
                self.isUp = self.isDown = False
            self.mapArr = self.type_of_collision(allBlock, 0, -int((self.jumpCount * abs(self.jumpCount)) / 2))
            self.jumpCount -= 1
        else:
            self.isUp = self.isDown = False
            self.set_jump(False)
            self.jumpCount = self.maxJump
