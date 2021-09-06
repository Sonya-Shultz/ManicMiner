# Клас для ігрового вікна
import pygame
from hero import GameHero
from gameMap import GameMap


class GameWindow:
    def __init__(self):
        pygame.init()

        self.infoObj = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.gameArea = pygame.Surface(self.infoObj)
        pygame.display.set_caption("Manic Miner v0.0.1")

        self.cubeCount = 20
        self.blockSize = int(self.infoObj[1] / 20)
        self.character = GameHero(0, 0, 0, 0, 0, False, 0)
        self.map = GameMap(int(self.infoObj[0] * 0.8 / self.blockSize), self.cubeCount)
        self.allBlocks = []
        self.allBlocksSt = [[10] * int(self.infoObj[0] * 0.8 / self.blockSize) for i in range(self.cubeCount)]
        self.gameObj = []
        self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)

        self.menu = True
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
        while self.menu or not self.character.isEnd:
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
            if keys[pygame.K_ESCAPE]:
                self.character.isEnd = True
                self.menu = False
            pygame.display.update()

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
                # зробить так, щоб була меню: переграти рівень, перегенерувати рівень, вийти
                self.character.isEnd = True
                # self.menu = True
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
            pygame.display.update()
            if self.character.timePoint <= 0:
                self.character.isEnd = True
            self.enemy_logic()
            self.draw_map(time)

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
            print(player.get_alpha())
        self.gameArea.blit(player, (self.character.chObj.x, self.character.chObj.y))
        self.win.blit(pygame.transform.scale(self.gameArea, self.infoObj), (0, 0))

    def enemy_death(self, time):
        for en in self.gameObj:
            if self.character.chObj.colliderect(en[0]) and time > 1000:
                time = 0
                self.character.life -= 1
                if self.character.life < 1:
                    self.character.isEnd = True
        return time

    def draw_statistic(self):
        x = int(self.infoObj[0] * 0.8 / self.blockSize) * self.blockSize
        timePos = (x, 2 * self.blockSize)
        lifePos = (x, 6 * self.blockSize)
        scorePos = (x, 10 * self.blockSize)
        self.gameArea.blit(pygame.transform.scale(self.statImg, (int(self.infoObj[0] - x), self.blockSize)), timePos)
        self.gameArea.blit(pygame.transform.scale(self.statImg, (int(self.infoObj[0] - x), self.blockSize)), lifePos)
        self.gameArea.blit(pygame.transform.scale(self.statImg, (int(self.infoObj[0] - x), self.blockSize)), scorePos)
