# Клас для персонажа гри
import pygame


class GameHero:
    def __init__(self, hight, width, x, y, speed, isJump, jumpCount):
        self.chHight = hight
        self.chWidth = width
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
        self.inAir = True
        self.isUp = False
        self.isDown = False
        self.isEnd = False
        self.life = 3
        self.isLeft = False
        self.timePoint = 100000
        self.isWin = False
        self.keysC = 0

    def start_pos(self, size, cubeC, map, allBlockSt):
        self.isUp = False
        self.isDown = False
        self.collision = []
        self.blockSize = int(size[1]/cubeC)
        self.chHight = int(self.blockSize * 1.8)
        self.chWidth = int(self.blockSize * 0.8)
        self.chSpeed = int(self.blockSize/3)
        self.isJump = False
        self.maxJump = int(size[1]/75)
        self.jumpCount = self.maxJump
        self.mapArr = map
        self.chObj = pygame.Rect(self.blockSize + 5, self.blockSize * 17 + 5, self.chWidth, self.chHight)
        self.chImg = [pygame.image.load("img/c1.png"), pygame.image.load("img/c2.png"),
                      pygame.image.load("img/c3.png"), pygame.image.load("img/c4.png")]
        self.collisionTypes = {'top': False, 'right': False, 'bottom': False, 'left': False}
        self.allBlockSt = allBlockSt
        self.isEnd = False
        self.life = 3
        self.timePoint = 100000
        self.isWin = False
        self.keysC = 0

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
                self.mapArr[y][x] = 0
                self.keysC += 1
            if blockMaterial == 5 and self.all_pick() == 0:
                self.isEnd = True
                self.isWin = True

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

    def all_pick(self):
        keyA = 0
        for i in self.mapArr:
            for j in i:
                if j == 4:
                    keyA += 1
        return keyA

