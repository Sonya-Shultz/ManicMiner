# Клас для ігрового вікна
import pygame
from hero import GameHero
from gameMap import GameMap
from pathCalc import PathCalc

# colors
# (150, 150, 150) - gray
# (250, 250, 250) - light gray
# (130, 180, 203) - light blue
# (168, 166, 126) - light green
# (253, 123, 31) - red
# (56, 56, 56) - black


class GameWindow:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.colors = [(150, 150, 150), (250, 250, 250), (97, 129, 141), (168, 166, 126), (253, 123, 31), (56, 56, 56)]
        self.font = pygame.font.Font("slkscr.ttf", 30)
        self.infoObj = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.gameArea = pygame.Surface(self.infoObj)
        pygame.display.set_caption("Manic Miner v0.0.1")

        self.cubeCount = 20
        self.blockSize = int(self.infoObj[1] / 20)
        self.character = GameHero(0, 0, 0, 0, 0, False, 0)
        self.map = GameMap(int(self.infoObj[0] * 0.75 / self.blockSize), self.cubeCount)
        self.startMapArr = [self.map.mapArr[i].copy() for i in range(len(self.map.mapArr))]
        self.allBlocks = []
        self.allBlocksSt = [[10] * int(self.infoObj[0] * 0.75 / self.blockSize) for i in range(self.cubeCount)]
        self.gameObj = []
        self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)

        self.menu = True
        self.menu = True
        self.subMenuTime = False
        self.algorithm = 1
        self.testImg = pygame.image.load("img/b1.png")
        self.cImg = pygame.image.load("img/b2.png")
        self.bImg = pygame.image.load("img/b3.png")
        self.dImg = pygame.image.load("img/b4.png")
        self.eImg = pygame.image.load("img/b5.png")
        self.en1Img = pygame.image.load("img/en1.png")
        self.en2Img = [pygame.image.load("img/en3m1.png"),
                       pygame.image.load("img/en3m2.png"), pygame.image.load("img/en3m3.png")]
        self.en3Img = pygame.image.load("img/en3.png")
        self.lImg = pygame.image.load("img/life.png")
        self.init_enemy()
        self.calc = {}
        self.way = []

        while self.menu or not self.character.isEnd or self.subMenuTime:
            self.run_menu_loop()
            self.run_game_loop()
        pygame.quit()

    def init_enemy(self):
        g_map = self.map.get_map()
        for a in range(len(g_map)):
            for b in range(len(g_map[a])):
                pos = int(b * self.blockSize), int(a * self.blockSize), int(self.blockSize), int(self.blockSize)
                if g_map[a][b] == 6:
                    self.gameArea.blit(pygame.transform.scale(self.en1Img, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                    self.gameObj.append([pygame.Rect(pos), 0, 6, 1])
                if g_map[a][b] == 7:
                    self.gameArea.blit(pygame.transform.scale(self.en2Img[0], (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                    self.gameObj.append([pygame.Rect(pos), 0, 7, 1])
                if g_map[a][b] == 8:
                    self.gameArea.blit(pygame.transform.scale(self.en3Img, (2 * self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                    self.gameObj.append([pygame.Rect(int(b * self.blockSize), int(a * self.blockSize),
                                                     2 * int(self.blockSize), int(self.blockSize)), 0, 8, 1])

    def run_menu_loop(self):
        while self.menu:
            pygame.time.delay(100)
            keys = pygame.key.get_pressed()
            self.win.fill(self.colors[3])
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
        text_menu = ['Q - exit from game', 'Return/enter - start game']
        self.gameArea.fill(self.colors[2])
        for i in range(len(text_menu)):
            menu_txt = self.font.render(text_menu[i], False, self.colors[5])
            x = int((self.infoObj[0] - menu_txt.get_width())/2)
            self.gameArea.blit(menu_txt, (x, (5 + i * 2) * self.blockSize))
        self.win.blit(pygame.transform.scale(self.gameArea, self.infoObj), (0, 0))

    def sub_menu(self, text):
        text_menu = [text, 'Q - exit from game', 'Return/enter - continue', 'R - start new game']
        time = 0
        while self.subMenuTime:
            pygame.time.delay(50)
            time += 50
            self.gameArea.fill(self.colors[2])
            for i in range(len(text_menu)):
                menu_txt = self.font.render(text_menu[i], False, self.colors[5])
                x = int((self.infoObj[0] - menu_txt.get_width()) / 2)
                self.gameArea.blit(menu_txt, (x, (5 + i * 2) * self.blockSize))
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
                self.map = GameMap(int(self.infoObj[0] * 0.75 / self.blockSize), self.cubeCount)
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
                    self.map = GameMap(int(self.infoObj[0] * 0.75 / self.blockSize), self.cubeCount)
                    self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                    self.startMapArr = [self.map.mapArr[i].copy() for i in range(len(self.map.mapArr))]
                    self.init_enemy()
                if self.character.life <= 0:
                    self.map.mapArr = [self.startMapArr[i].copy() for i in range(len(self.startMapArr))]
                    self.allBlocksSt = [[10] * int(self.infoObj[0] * 0.75 / self.blockSize) for i in
                                        range(self.cubeCount)]
                    self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                    time = 0
                self.character.isEnd = False
                self.subMenuTime = False
                self.menu = False

    def run_game_loop(self):
        time = 0
        while not self.character.isEnd:
            self.gameArea = pygame.Surface(self.infoObj)
            pygame.time.delay(50)
            time += 50
            self.character.timePoint -= 50
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.character.isEnd = True
                    self.menu = False
            keys = pygame.key.get_pressed()
            self.calc = PathCalc(self.map.mapArr)
            self.way = self.calc.start_smpl_bfs(self.get_ch_pos(self.character.chObj.x, self.character.chObj.y))
            my_keys = self.ch_automatic_move(self.way)
            all_way = self.find_ch_for_enemy()
            if keys[pygame.K_ESCAPE]:
                self.character.isEnd = True
                self.subMenuTime = True
                self.sub_menu('PAUSE')
            elif keys[pygame.K_r]:
                self.map.mapArr = [self.startMapArr[i].copy() for i in range(len(self.startMapArr))]
                self.allBlocksSt = [[10] * int(self.infoObj[0] * 0.75 / self.blockSize) for i in range(self.cubeCount)]
                self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                time = 0
            elif keys[pygame.K_q]:
                time = 0
                self.gameObj = []
                self.allBlocks = []
                self.map = GameMap(int(self.infoObj[0] * 0.75 / self.blockSize), self.cubeCount)
                self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map(), self.allBlocksSt)
                self.startMapArr = [self.map.mapArr[i].copy() for i in range(len(self.map.mapArr))]
                self.init_enemy()
            else:
                '''if keys[pygame.K_z]:
                    self.algorithm = (self.algorithm + 1) % 3'''
                if keys[pygame.K_LEFT] or keys[pygame.K_a] or my_keys[0]:
                    self.map.mapArr = self.character.type_of_collision(self.allBlocks, -self.character.chSpeed + 2, 0)
                    self.character.isLeft = True
                if keys[pygame.K_RIGHT] or keys[pygame.K_d] or my_keys[1]:
                    self.character.isLeft = False
                    self.map.mapArr = self.character.type_of_collision(self.allBlocks, self.character.chSpeed - 2, 0)
                if not self.character.isJump:
                    if (keys[pygame.K_SPACE] or my_keys[2]) and not self.character.inAir:
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
                self.sub_menu('YOU WIN! YOU SCORE: '+str(int(self.character.timePoint / 50) + 500 * self.character.keysC))
            self.enemy_logic(all_way)
            '''if time % 200 == 0:
                self.calc = PathCalc(self.map.mapArr)
                self.way = self.calc.start_smpl_bfs(self.get_ch_pos())'''
            self.draw_map(time, self.way, all_way)
            pygame.display.update()

    def ch_automatic_move(self, way):
        keys = [0, 0, 0]
        if len(way) > 0:
            x1 = way[0][0]
            if self.character.chObj.x > x1 * self.blockSize and self.character.isLeft:
                keys[0] = 1
            elif self.character.chObj.x < x1 * self.blockSize and not self.character.isLeft:
                keys[1] = 1
        if len(way) > 1:
            x1 = way[0][0]
            x2 = way[1][0]
            y1 = way[0][1]
            y2 = way[1][1]
            if x1 > x2:
                keys[0] = 1  # left
            elif x1 < x2:
                keys[1] = 1  # right
            elif len(way) > 2 and x1 > way[2][0]:
                keys[0] = 1  # left
            elif len(way) > 2 and x1 < way[2][0]:
                keys[1] = 1  # right
            if y1 > y2:
                keys[2] = 1  # jump
        return keys

    def draw_way(self, way, war):
        for i in range(len(way)):
            x = way[i][0]
            y = way[i][1]
            x_size = int(self.blockSize * (1 - (i+1) / len(way))) + 3
            y_size = int((self.blockSize - x_size)/2)
            way_pos = (x*self.blockSize+y_size, y*self.blockSize+y_size, x_size, x_size)
            if war == 0:
                pygame.draw.rect(self.gameArea, (i * 2 % 255, i * war % 255, i * 1 % 255), pygame.Rect(way_pos))
            else:
                r = max(int(x_size/2)-5, 5)
                pygame.draw.circle(self.gameArea, ((100 + i * 2) % 255, (150 + war) % 255, (100 + i * 1) % 255),
                                   ((x+0.5)*self.blockSize, (y+0.5)*self.blockSize), r)

    def find_ch_for_enemy(self):
        all_way = []
        for en in self.gameObj:
            if en[2] != 6:
                self.calc = PathCalc(self.map.mapArr)
                en_pos = self.get_ch_pos(en[0].x, en[0].y)
                en_pos[1] -= 1
                en_way = self.calc.start_a_star(en_pos, self.get_ch_pos(self.character.chObj.x, self.character.chObj.y))
                all_way.append(en_way)
            else:
                all_way.append([])
        return all_way

    def get_ch_pos(self, x, y):
        x = int(x / self.blockSize)
        y = int(y / self.blockSize) + 1
        if y >= self.cubeCount:
            y = self.cubeCount - 1
        return [x, y]

    def decide_to_move(self, en, en_id, all_way):
        if len(all_way) > en_id > -1 and len(all_way[en_id]) > 0:
            if -5 < all_way[en_id][len(all_way[en_id])-1][1] - all_way[en_id][0][1] < 5:
                if all_way[en_id][len(all_way[en_id])-1][0] > all_way[en_id][0][0]:
                    en[1] = 0
                else:
                    en[1] = 1

        if en[1] == 0:
            en[0].x += int(self.character.chSpeed * 0.75)
        else:
            en[0].x -= int(self.character.chSpeed * 0.75)

        return en

    def enemy_logic(self, all_way):
        for en in self.gameObj:
            if en[2] != 6:
                if en[2] == 7:
                    on_platform = False
                    en[0].y += int(self.character.chSpeed * 0.75)
                    for block in self.allBlocks:
                        if en[0].colliderect(block):
                            on_platform = True
                            en[0].bottom = block.top
                            en[3] = 1

                    if not on_platform:
                        en[3] = 0

                en = self.decide_to_move(en, self.gameObj.index(en), all_way)

                for block in self.allBlocks:
                    if en[0].colliderect(block):
                        if en[1] == 0:
                            en[0].right = block.left
                        else:
                            en[0].left = block.right
                        en[1] = (en[1] + 1) % 2

                for q in self.gameObj:
                    if en[0].colliderect(q[0]) and q != en:
                        if en[1] == 0:
                            en[0].right = q[0].left
                        else:
                            en[0].left = q[0].right
                        en[1] = (en[1] + 1) % 2

    def draw_enemy(self, time):
        for el in self.gameObj:
            if el[2] == 6:
                self.gameArea.blit(pygame.transform.scale(self.en1Img, (self.blockSize, self.blockSize)),
                                   (el[0].x, el[0].y))
            elif el[2] == 7:
                time_inner = time % 1500
                pos = 0
                if time_inner < 300:
                    pos = 0
                elif time_inner < 600 or 1200 <= time_inner < 1500:
                    pos = 1
                elif time_inner < 900:
                    pos = 2
                if el[1] == 0:
                    self.gameArea.blit(pygame.transform.scale(pygame.transform.flip(self.en2Img[pos], True, False),
                                                              (self.blockSize, self.blockSize)),
                                       (el[0].x, el[0].y))
                else:
                    self.gameArea.blit(pygame.transform.scale(self.en2Img[pos], (self.blockSize, self.blockSize)),
                                   (el[0].x, el[0].y))
            elif el[2] == 8:
                self.gameArea.blit(pygame.transform.scale(self.en3Img, (2 * self.blockSize, self.blockSize)),
                                   (el[0].x, el[0].y))

    def draw_map(self, time, way, all_way):
        self.allBlocks = []
        self.gameArea.fill(self.colors[3])
        g_map = self.map.get_map()
        for a in range(len(g_map)):
            for b in range(len(g_map[a])):
                pos = int(b * self.blockSize), int(a * self.blockSize), int(self.blockSize), int(self.blockSize)
                if g_map[a][b] == 1:
                    self.gameArea.blit(pygame.transform.scale(self.testImg, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                if g_map[a][b] == 2:
                    self.gameArea.blit(pygame.transform.scale(self.cImg, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                if g_map[a][b] == 3:
                    self.gameArea.blit(pygame.transform.scale(self.bImg, (self.blockSize,
                                                                          int(self.blockSize * self.allBlocksSt[a][
                                                                              b] / 10))),
                                       (self.blockSize * b, self.blockSize * a))
                if g_map[a][b] == 4:
                    self.gameArea.blit(pygame.transform.scale(self.dImg, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                if g_map[a][b] == 5:
                    self.gameArea.blit(pygame.transform.scale(self.eImg, (self.blockSize, self.blockSize)),
                                       (self.blockSize * b, self.blockSize * a))
                if 0 < g_map[a][b] < 6 and self.allBlocksSt[a][b] > 0:
                    self.allBlocks.append(pygame.Rect(pos))

        self.draw_way(way, 0)
        for en in range(len(all_way)):
            self.draw_way(all_way[en], en+1)
        self.draw_enemy(time)
        self.draw_statistic()
        self.draw_ch(time)
        self.win.blit(pygame.transform.scale(self.gameArea, self.infoObj), (0, 0))

    def draw_ch(self, time):
        in_time = time % 1200
        pos = 0
        if in_time < 200 or 400 <= in_time < 600:
            pos = 0
        elif in_time < 400:
            pos = 1
        elif in_time < 800 or 1000 <= in_time < 1200:
            pos = 2
        elif in_time < 1000:
            pos = 3
        if self.character.isLeft:
            player = pygame.transform.scale(pygame.transform.flip(self.character.chImg[pos], True, False),
                                                                    (self.character.chWidth, self.character.chHight))
        else:
            player = pygame.transform.scale(self.character.chImg[pos], (self.character.chWidth, self.character.chHight))
        if time < 1000:
            if time % 20 == 0:
                player.set_alpha(255)
            if time % 40 == 0:
                player.set_alpha(100)
        self.gameArea.blit(player, (self.character.chObj.x, self.character.chObj.y))

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
        x = int(self.infoObj[0] * 0.75 / self.blockSize) * self.blockSize
        pygame.draw.rect(self.gameArea, self.colors[2], pygame.Rect(x, 0, self.infoObj[0]-x, self.infoObj[1]))
        time_txt = self.font.render('AIR', False, self.colors[5])
        time_pos = (x, 2 * self.blockSize, int(self.infoObj[0] - x), self.blockSize)
        time_inner_pos = (x + time_txt.get_width() + 5, 2 * self.blockSize + 5,
                        int(self.infoObj[0] - x - time_txt.get_width() - 10), self.blockSize - 10)
        time_fill_pos = (x + time_txt.get_width() + 5, 2 * self.blockSize + 5, int((self.infoObj[0] - x
                                - time_txt.get_width() - 10) * self.character.timePoint / 100000), self.blockSize - 10)
        score_pos = (x, 6 * self.blockSize, int(self.infoObj[0] - x), self.blockSize)

        pygame.draw.rect(self.gameArea, self.colors[3], pygame.Rect(time_pos))
        pygame.draw.rect(self.gameArea, self.colors[4], pygame.Rect(time_fill_pos))
        pygame.draw.rect(self.gameArea, self.colors[1], pygame.Rect(time_inner_pos), 3)
        self.gameArea.blit(time_txt, (x, 2 * self.blockSize + 5))

        for i in range(self.character.life):
            life_pos = (x + i * int((self.infoObj[0] - x) / 3), 7 * self.blockSize,)
            life_size = (int((self.infoObj[0] - x) / 3), int((self.infoObj[0] - x) / 3))
            self.gameArea.blit(pygame.transform.scale(self.lImg, life_size), life_pos)

        score_txt = self.font.render('SCORE ' + str(int(self.character.timePoint / 50) + 500 * self.character.keysC),
                                    False, self.colors[5])
        pygame.draw.rect(self.gameArea, self.colors[3], pygame.Rect(score_pos))
        x_score = int((self.infoObj[0] - x - score_txt.get_width()) / 2)
        self.gameArea.blit(score_txt, (x + x_score, 6 * self.blockSize + 5))

        text_menu = ['R - replay lvl', 'Q - generate again', 'Esc - exit to menu']
        for i in range(len(text_menu)):
            menu_txt = self.font.render(text_menu[i], False, self.colors[5])
            self.gameArea.blit(menu_txt, (x + 5, (11 + i*1) * self.blockSize))

        algorithm_menu = ['DFS', 'BFS', 'UCS']
        algorithm_txt = self.font.render("Algorithm: " + algorithm_menu[self.algorithm], False, self.colors[5])
        self.gameArea.blit(algorithm_txt, (x + 5, 15 * self.blockSize))
        '''help_txt = self.font.render("Z - change algorithm", False, self.colors[5])
        self.gameArea.blit(help_txt, (x + 5, 16 * self.blockSize))'''
        help_txt = self.font.render("Path len "+str(len(self.way)), False, self.colors[5])
        self.gameArea.blit(help_txt, (x + 5, 16 * self.blockSize))
