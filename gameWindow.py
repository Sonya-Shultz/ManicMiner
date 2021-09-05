# Клас для ігрового вікна
import pygame
from hero import GameHero
from gameMap import GameMap


class GameWindow:
    def __init__(self):
        pygame.init()

        self.infoObj = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Manic Miner v0.0.1")

        self.cubeCount = 20
        self.blockSize = int(self.infoObj[1]/20)
        self.character = GameHero(0, 0, 0, 0, 0, False, 0)
        self.map = GameMap(int(self.infoObj[0] / self.blockSize), self.cubeCount)
        self.character.start_pos(self.infoObj, self.cubeCount, self.map.get_map())

        self.run = False
        self.menu = True

        while self.menu or self.run:
            self.run_menu_loop()
            self.run_game_loop()
        pygame.quit()

    def run_menu_loop(self):
        while self.menu:
            pygame.time.delay(100)
            keys = pygame.key.get_pressed()
            self.win.fill((130, 180, 203))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    self.menu = False
            if keys[pygame.K_RETURN]:
                self.menu = False
                self.run = True
            if keys[pygame.K_ESCAPE]:
                self.run = False
                self.menu = False
            pygame.display.update()

    def run_game_loop(self):
        while self.run:
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    self.menu = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                # зробить так, щоб була меню: переграти рівень, перегенерувати рівень, вийти
                self.run = False
                # self.menu = True
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.character.change_pos_x(-self.character.chSpeed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.character.change_pos_x(self.character.chSpeed)
            if not self.character.isJump:
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.character.change_pos_y(self.character.chSpeed)
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.character.change_pos_y(-self.character.chSpeed)
                if keys[pygame.K_SPACE]:
                    self.character.set_jump(True)
            else:
                self.character.jump_proc()
            self.win.fill((0, 0, 0))
            pygame.draw.rect(self.win, (45, 110, 146), self.character.get_pos_data())
            self.draw_map()
            pygame.display.update()

    def draw_map(self):
        gMap = self.map.get_map()
        for a in range(len(gMap)):
            for b in range(len(gMap[a])):
                if gMap[a][b] == 1:
                    pos = int(b * self.blockSize), int(a * self.blockSize), int(self.blockSize), int(self.blockSize)
                    pygame.draw.rect(self.win, (a*3, (a+b)*3, b*3), pos)


