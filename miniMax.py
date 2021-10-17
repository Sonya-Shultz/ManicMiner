# 0 - left, 1 - right, 2 - jump, 3 - not move
import copy
import random
from pathCalc import PathCalc


class MiniMaxAlg:
    def __init__(self, mape, all_block, enemy, character):
        self.way = []
        self.block_map = [mape[i].copy() for i in range(len(mape))]
        self.all_block = [all_block[i].copy() for i in range(len(all_block))]
        self.enemy_map = [enemy[i].copy() for i in range(len(enemy))]
        self.character = character.copy_ch()

    class MinimaxTree:
        def __init__(self, ch, bl_map, all_bl, en):
            self.max_dep = 3
            self.cur_dep = 0
            self.position = 0
            self.score = None
            self.parent = None
            self.child = []
            self.all_way = []
            self.block_map = [bl_map[i].copy() for i in range(len(bl_map))]
            self.all_block = [all_bl[i].copy() for i in range(len(all_bl))]
            self.enemy_map = [en[i].copy() for i in range(len(en))]
            self.character = ch.copy_ch()

        def set_start_data(self, new_dep, pos, parent):
            self.cur_dep = new_dep
            self.position = pos
            self.parent = parent

    def minimax_calc(self):
        first_node = self.MinimaxTree(self.character, self.block_map, self.all_block, self.enemy_map)
        self.minimax(first_node)
        first_node.all_way.reverse()
        #print(first_node.all_way)

    def minimax(self, new_node):
        if new_node.parent is not None:
            new_node.all_way = new_node.parent.all_way.copy()
        new_node.all_way.append(new_node.position)
        is_terminal, is_win = self.is_terminal_node(new_node)
        if is_terminal:
            new_node.score = 500
            return new_node.all_way
            # тут треба написать таке, щоб воно рахувало оцінку відносного того, де вороги будуть, де чел буде і коли
        if new_node.cur_dep == new_node.max_dep:
            new_node.score = 100
            return new_node.all_way
            # тут треба написать таке, щоб воно рахувало оцінку відносного того, де вороги будуть, де чел буде і коли
            # і не забудь що час в залежності від довжини "шляху"
            # тобто грати в гру без показу цього
            # костиль: не обновлять екран, але пройтись грою по ньому, а потім повернути все до записаного значення
            # дописати алг на тему розуміння термінальних станів
        for i in range(0, 4):
            child_node = self.MinimaxTree(new_node.character, new_node.block_map, new_node.all_block,
                                          new_node.enemy_map)
            child_node.set_start_data(new_node.cur_dep + 1, i, new_node)
            new_node.child.append(child_node)
            self.calc_one_step(i, child_node.cur_dep, child_node.block_map, child_node.all_block, child_node.character, child_node.enemy_map)
            new_node.all_way = self.minimax(child_node)
        if new_node.cur_dep % 2 == 0:
            max_score = 0
            index = 0
            for el in range(len(new_node.child)):
                if new_node.child[el].score > max_score:
                    max_score = new_node.child[el].score
                    index = el
            new_node.all_way = new_node.child[index].all_way
            new_node.score = new_node.child[index].score
        else:
            min_score = 100000
            index = 0
            for el in range(len(new_node.child)):
                if new_node.child[el].score < min_score:
                    min_score = new_node.child[el].score
                    index = el
            new_node.all_way = new_node.child[index].all_way
            new_node.score = new_node.child[index].score
        return new_node.all_way

    @staticmethod
    def is_terminal_node(node):
        if node.character.life < 1 or node.character.timePoint < 1:
            return True, False
        if node.character.isWin:
            return True, True
        # якщо це термінальне, бо смерть, то 2ийпараметр - фолс
        return False, False

    def calc_one_step(self, move_direction, cur_dep, block_map, all_block, character, enemy):
        character.timePoint -= 50
        all_way = self.find_ch_for_enemy(enemy, block_map, character)
        if move_direction == 0:
            block_map = character.type_of_collision(all_block, -character.chSpeed + 2, 0)
            character.isLeft = True
        elif move_direction == 1:
            character.isLeft = False
            block_map = character.type_of_collision(all_block, character.chSpeed - 2, 0)
        if not character.isJump:
            if (move_direction == 2) and not self.character.inAir:
                character.isUp = True
                character.inAir = True
                character.set_jump(True)
            if not character.collisionTypes['bottom']:
                character.inAir = True
                character.isDown = True
                block_map = character.type_of_collision(all_block, 0, 3 * character.chSpeed)
        else:
            character.do_jump(all_block)
        self.character = self.enemy_death(self.enemy_map, self.character)
        if character.timePoint <= 0:
            character.isEnd = True
            character.isWin = False
        if character.isWin:
            character.isEnd = True
        self.enemy_logic(all_way, enemy, all_block, character)

    def one_game_step(self, node):
        return self.calc_one_step(node.position, node.cur_dep, node.block_map, node.all_block, node.character,
                                  node.enemy_map)

    @staticmethod
    def find_ch_for_enemy(enemy, map_arr, character):
        all_way = []
        for en in enemy:
            if en[2] != 6:
                calc = PathCalc(map_arr)
                en_pos = [int(en[0].x/character.blockSize), int(en[0].y/character.blockSize)]
                en_way = calc.start_a_star(en_pos, [int(character.chObj.x/character.blockSize),
                                                    int(character.chObj.y/character.blockSize)])
                all_way.append(en_way)
            else:
                all_way.append([])
        return all_way

    @staticmethod
    def enemy_death(enemy, character):
        for en in enemy:
            if character.chObj.colliderect(en[0]):  # and time > 1000:
                # time = 0
                character.life -= 1
                if character.life < 1:
                    character.isEnd = True
                    character.isWin = False
        return character

    def enemy_logic(self, all_way, enemy, all_block, character):
        for en in enemy:
            if en[2] != 6:
                if en[2] == 7:
                    on_platform = False
                    en[0].y += int(character.chSpeed * 0.75)
                    for block in all_block:
                        if en[0].colliderect(block[0]):
                            on_platform = True
                            en[0].bottom = block[0].top
                            en[3] = 1

                    if not on_platform:
                        en[3] = 0

                en = self.decide_to_move(character.chSpeed, en, enemy.index(en), all_way)

                for block in all_block:
                    if en[0].colliderect(block[0]):
                        if en[1] == 0:
                            en[0].right = block[0].left
                        else:
                            en[0].left = block[0].right
                        en[1] = (en[1] + 1) % 2

                for q in enemy:
                    if en[0].colliderect(q[0]) and q != en:
                        if en[1] == 0:
                            en[0].right = q[0].left
                        else:
                            en[0].left = q[0].right
                        en[1] = (en[1] + 1) % 2

    @staticmethod
    def decide_to_move(speed, en, en_id, all_way):
        if en[2] == 8:
            en[1] = random.randint(0, 1)
        else:
            if len(all_way) > en_id > -1 and len(all_way[en_id]) > 0:
                if -5 < all_way[en_id][len(all_way[en_id])-1][1] - all_way[en_id][0][1] < 5:
                    if all_way[en_id][len(all_way[en_id])-1][0] > all_way[en_id][0][0]:
                        en[1] = 0
                    else:
                        en[1] = 1

        if en[1] == 0:
            en[0].x += int(speed * 0.75)
        else:
            en[0].x -= int(speed * 0.75)

        return en
