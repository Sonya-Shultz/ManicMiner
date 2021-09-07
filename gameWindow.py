# Клас для ігрового вікна
import pygame
from hero import GameHero
from gameMap import GameMap


# colors
# (150, 150, 150) - gray
# (250, 250, 250) - light gray
# (130, 180, 203) - light blue
# (50, 130, 70) - light green
# (190, 100, 80) - red

class GameWindow:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.colors = [(150, 150, 150), (250, 250, 250), (130, 180, 203), (50, 130, 70), (190, 100, 80)]
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.infoObj = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.gameArea = pygame.Surface(self.infoObj)
        pygame.display.set_caption("Manic Miner v0.0.1")

        self.cubeCount = 20
        self.blockSize = int(self.infoObj[1] / 20)
        self.character = GameHero(0, 0, 0, 0, 0, False, 0)
        self.map = GameMap(int(self.infoObj[0] * 0.8 / self.blockSize), self.cubeCount)
        self.startMapArr = [self.map.mapArr[i].copy() for i in range(len(self.map.mapArr))]
        self.allBlocks = []
        self.allBlocksSt = [[10] * int(self.infoObj[0] * 0.8 / self.blockSize) for i in range(self.cubeCount)]
        self.gameObj = []
        self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)

        self.menu = True
        self.subMenuTime = False
        self.testImg = pygame.image.load("a.png")
        self.cImg = pygame.image.load("c.png")
        self.bImg = pygame.image.load("b.png")
        self.dImg = pygame.image.load("d.png")
        self.eImg = pygame.image.load("e.png")
        self.en1Img = pygame.image.load("en1.png")
        self.en2Img = pygame.image.load("en2.png")
        self.en3Img = pygame.image.load("en3.png")
        self.statImg = pygame.image.load("stat.png")
        self.init_enemy()
        while self.menu or not self.character.isEnd or self.subMenuTime:
            self.run_menu_loop()
            self.run_game_loop()
        pygame.quit()

    def init_enemy(self):
        gMap = self.map.get_map()
        for a in range(len(gMap)):
            for b in range(len(gMap[a])):
                pos = int(b * self.blockSize), int(a * self.blockSize), int(self.blockSize), int(self.blockSize)
                if gMap[a][b] == 6:
                    self.gameArea.blit(pygame.transform.scale(self.en1Img, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                    self.gameObj.append([pygame.Rect(pos), 0, 6])
                if gMap[a][b] == 7:
                    self.gameArea.blit(pygame.transform.scale(self.en2Img, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                    self.gameObj.append([pygame.Rect(pos), 0, 7])
                if gMap[a][b] == 8:
                    self.gameArea.blit(pygame.transform.scale(self.en3Img, (2 * self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                    self.gameObj.append([pygame.Rect(int(b * self.blockSize), int(a * self.blockSize),
                                                     2 * int(self.blockSize), int(self.blockSize)), 0, 8])

    def run_menu_loop(self):
        while self.menu:
            pygame.time.delay(100)
            keys = pygame.key.get_pressed()
            self.win.fill((130, 180, 203))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.character.isEnd = True
                    self.menu = False
            if keys[pygame.K_RETURN]:
                self.menu = False
                self.character.isEnd = False
            if keys[pygame.K_q]:
                self.character.isEnd = True
                self.menu = False
            self.draw_menu()
            pygame.display.update()

    def draw_menu(self):
        textMenu = ['Q - exit from game', 'Return/enter - start game']
        self.gameArea.fill((130, 180, 203))
        for i in range(len(textMenu)):
            menuTxt = self.font.render(textMenu[i], False, (0, 0, 0))
            x = int((self.infoObj[0] - menuTxt.get_width())/2)
            self.gameArea.blit(menuTxt, (x, (5 + i * 2) * self.blockSize))
        self.win.blit(pygame.transform.scale(self.gameArea, self.infoObj), (0, 0))

    def sub_menu(self, text):
        textMenu = [text, 'Q - exit from game', 'Return/enter - continue', 'R - start new game']
        time = 0
        while self.subMenuTime:
            pygame.time.delay(50)
            time += 50
            self.gameArea.fill((130, 180, 203))
            for i in range(len(textMenu)):
                menuTxt = self.font.render(textMenu[i], False, (0, 0, 0))
                x = int((self.infoObj[0] - menuTxt.get_width()) / 2)
                self.gameArea.blit(menuTxt, (x, (5 + i * 2) * self.blockSize))
            self.win.blit(pygame.transform.scale(self.gameArea, self.infoObj), (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.character.isEnd = True
                    self.menu = False
                    self.subMenuTime = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                self.character.isEnd = True
                self.subMenuTime = False
                self.menu = True
            if keys[pygame.K_r]:
                time = 0
                self.gameObj = []
                self.allBlocks = []
                self.map = GameMap(int(self.infoObj[0] * 0.8 / self.blockSize), self.cubeCount)
                self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                self.startMapArr = [self.map.mapArr[i].copy() for i in range(len(self.map.mapArr))]
                self.init_enemy()
                self.character.isEnd = False
                self.subMenuTime = False
                self.menu = False
            if keys[pygame.K_RETURN]:
                if self.character.isWin:
                    time = 0
                    self.gameObj = []
                    self.allBlocks = []
                    self.map = GameMap(int(self.infoObj[0] * 0.8 / self.blockSize), self.cubeCount)
                    self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                    self.startMapArr = [self.map.mapArr[i].copy() for i in range(len(self.map.mapArr))]
                if self.character.life <= 0:
                    self.map.mapArr = [self.startMapArr[i].copy() for i in range(len(self.startMapArr))]
                    self.allBlocksSt = [[10] * int(self.infoObj[0] * 0.8 / self.blockSize) for i in
                                        range(self.cubeCount)]
                    self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                    time = 0
                self.character.isEnd = False
                self.subMenuTime = False
                self.menu = False

    def run_game_loop(self):
        time = 0
        while not self.character.isEnd:
            pygame.time.delay(50)
            time += 50
            self.character.timePoint -= 50
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.character.isEnd = True
                    self.menu = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.character.isEnd = True
                self.subMenuTime = True
                self.sub_menu('PAUSE')
            elif keys[pygame.K_r]:
                self.map.mapArr = [self.startMapArr[i].copy() for i in range(len(self.startMapArr))]
                self.allBlocksSt = [[10] * int(self.infoObj[0] * 0.8 / self.blockSize) for i in range(self.cubeCount)]
                self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                time = 0
            elif keys[pygame.K_q]:
                time = 0
                self.gameObj = []
                self.allBlocks = []
                self.map = GameMap(int(self.infoObj[0] * 0.8 / self.blockSize), self.cubeCount)
                self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                self.startMapArr = [self.map.mapArr[i].copy() for i in range(len(self.map.mapArr))]
                self.init_enemy()
            else:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.map.mapArr = self.character.type_of_collision(self.allBlocks, -self.character.chSpeed, 0)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.map.mapArr = self.character.type_of_collision(self.allBlocks, self.character.chSpeed, 0)
                if not self.character.isJump:
                    if keys[pygame.K_SPACE] and not self.character.inAir:
                        self.character.isUp = True
                        self.character.inAir = True
                        self.character.set_jump(True)
                    if not self.character.collisionTypes['bottom']:
                        self.character.inAir = True
                        self.character.isDown = True
                        self.map.mapArr = self.character.type_of_collision(self.allBlocks, 0, 3 * self.character.chSpeed)
                else:
                    self.character.do_jump(self.allBlocks)
                time = self.enemy_death(time)
            if self.character.timePoint <= 0:
                self.character.isEnd = True
                self.character.isWin = False
                self.subMenuTime = True
                self.sub_menu('YOU LOSE (')
            if self.character.isWin:
                self.character.isEnd = True
                self.subMenuTime = True
                self.sub_menu('YOU WIN!')
            self.enemy_logic()
            self.draw_map(time)
            pygame.display.update()

    def enemy_logic(self):
        for en in self.gameObj:
            if en[2] != 6:
                if en[1] == 0:
                    en[0].x += int(self.character.chSpeed * 0.8)
                else:
                    en[0].x -= int(self.character.chSpeed * 0.8)
                for block in self.allBlocks:
                    if en[0].colliderect(block):
                        if en[1] == 0:
                            en[0].right = block.left
                            en[1] = 1
                        else:
                            en[0].left = block.right
                            en[1] = 0
                for q in self.gameObj:
                    if en[0].colliderect(q[0]) and q != en:
                        if en[1] == 0:
                            en[0].right = q[0].left
                            en[1] = 1
                        else:
                            en[0].left = q[0].right
                            en[1] = 0
                en[0].y += 5
                if en[2] == 7:
                    onPlatform = False
                    for block in self.allBlocks:
                        if en[0].colliderect(block):
                            onPlatform = True
                    if not onPlatform:
                        if en[1] == 0:
                            en[1] = 1
                        else:
                            en[1] = 0
                en[0].y -= 5

    def draw_enemy(self):
        for el in self.gameObj:
            if el[2] == 6:
                self.gameArea.blit(pygame.transform.scale(self.en1Img, (self.blockSize, self.blockSize)),
                                   (el[0].x, el[0].y))
            elif el[2] == 7:
                self.gameArea.blit(pygame.transform.scale(self.en2Img, (self.blockSize, self.blockSize)),
                                   (el[0].x, el[0].y))
            elif el[2] == 8:
                self.gameArea.blit(pygame.transform.scale(self.en3Img, (2 * self.blockSize, self.blockSize)),
                                   (el[0].x, el[0].y))

    def draw_map(self, time):
        self.allBlocks = []
        self.gameArea.fill((50, 130, 70))
        gMap = self.map.get_map()
        for a in range(len(gMap)):
            for b in range(len(gMap[a])):
                pos = int(b * self.blockSize), int(a * self.blockSize), int(self.blockSize), int(self.blockSize)
                if gMap[a][b] == 1:
                    self.gameArea.blit(pygame.transform.scale(self.testImg, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                if gMap[a][b] == 2:
                    self.gameArea.blit(pygame.transform.scale(self.cImg, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                if gMap[a][b] == 3:
                    self.gameArea.blit(pygame.transform.scale(self.bImg, (self.blockSize,
                                                                          int(self.blockSize * self.allBlocksSt[a][
                                                                              b] / 10))),
                                       (self.blockSize * b, self.blockSize * a))
                if gMap[a][b] == 4:
                    self.gameArea.blit(pygame.transform.scale(self.dImg, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                if gMap[a][b] == 5:
                    self.gameArea.blit(pygame.transform.scale(self.eImg, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                if 0 < gMap[a][b] < 6 and self.allBlocksSt[a][b] > 0:
                    self.allBlocks.append(pygame.Rect(pos))

        self.draw_enemy()
        self.draw_statistic()
        player = pygame.transform.scale(self.character.chImg, (self.character.chWidth, self.character.chHight))
        if time < 1000:
            if time % 20 == 0:
                player.set_alpha(255)
            if time % 40 == 0:
                player.set_alpha(100)
        self.gameArea.blit(player, (self.character.chObj.x, self.character.chObj.y))
        self.win.blit(pygame.transform.scale(self.gameArea, self.infoObj), (0, 0))

    def enemy_death(self, time):
        for en in self.gameObj:
            if self.character.chObj.colliderect(en[0]) and time > 1000:
                time = 0
                self.character.life -= 1
                if self.character.life < 1:
                    self.character.isEnd = True
                    self.character.isWin = False
                    self.subMenuTime = True
                    self.sub_menu('YOU LOSE!')
        return time

    def draw_statistic(self):
        x = int(self.infoObj[0] * 0.8 / self.blockSize) * self.blockSize
        pygame.draw.rect(self.gameArea, self.colors[2], pygame.Rect(x, 0, self.infoObj[0]-x, self.infoObj[1]))
        timeTxt = self.font.render('AIR', False, (0, 0, 0))
        timePos = (x, 2 * self.blockSize, int(self.infoObj[0] - x), self.blockSize)
        timeInnerPos = (x + timeTxt.get_width() + 5, 2 * self.blockSize + 5,
                        int(self.infoObj[0] - x - timeTxt.get_width() - 10), self.blockSize - 10)
        timeFillPos = (x + timeTxt.get_width() + 5, 2 * self.blockSize + 5, int((self.infoObj[0] - x -
                                    timeTxt.get_width() - 10) * self.character.timePoint / 100000), self.blockSize - 10)
        scorePos = (x, 6 * self.blockSize, int(self.infoObj[0] - x), self.blockSize)

        pygame.draw.rect(self.gameArea, self.colors[0], pygame.Rect(timePos))
        pygame.draw.rect(self.gameArea, self.colors[4], pygame.Rect(timeFillPos))
        pygame.draw.rect(self.gameArea, self.colors[1], pygame.Rect(timeInnerPos), 3)
        self.gameArea.blit(timeTxt, (x, 2 * self.blockSize))

        for i in range(self.character.life):
            lifePos = (x + i * int((self.infoObj[0] - x) / 3), 7 * self.blockSize,)
            lifeSize = (int((self.infoObj[0] - x) / 3), 3 * self.blockSize)
            self.gameArea.blit(pygame.transform.scale(self.character.chImg, lifeSize), lifePos)

        scoreTxt = self.font.render('SCORE ' + str(int(self.character.timePoint / 50)), False, (0, 0, 0))
        pygame.draw.rect(self.gameArea, self.colors[0], pygame.Rect(scorePos))
        xScore = int((self.infoObj[0] - x - scoreTxt.get_width()) / 2)
        self.gameArea.blit(scoreTxt, (x + xScore, 6 * self.blockSize))

        textMenu = ['R - replay lvl', 'Q - generate again', 'Esc - exit to menu']
        for i in range(len(textMenu)):
            menuTxt = self.font.render(textMenu[i], False, (0, 0, 0))
            self.gameArea.blit(menuTxt, (x + 5, (11 + i*1) * self.blockSize))
