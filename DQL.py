
# 1-left, 2-right, 3-up, 4-not move, 5-l+u, 6-r+u
# 0-4-dist to nearest enemy, 5-9-dist to nearest key, 10-key count, 11-15-dist to exit, 16-isJump, 17-time left,
# 18 -lives
# 19-28-blocks around(3down, 3up, 2 left and 2right)
import random


class InputData:
    def __init__(self):
        self.gamer_pos = [0, 0]
        self.keys_pos = []
        self.enemy_pos = []
        self.exit_pos = []
        self.map = []
        self.lives = 0
        self.time_left = 0
        self.is_jump = 0

    def set_data(self, g_pos, e_pos, map_c, lives, time_left, jump):
        self.gamer_pos = g_pos
        self.enemy_pos = e_pos
        self.map = map_c
        self.lives = lives
        self.time_left = time_left
        self.is_jump = jump
        self.find_on_map()

    def calc_dist(self):
        data = []

        en_dist = [self.pif_dist(i, self.gamer_pos) for i in self.enemy_pos]
        en_dist_h = min(en_dist)
        en_dist_p = self.enemy_pos[en_dist.index(en_dist_h)]
        en_up = 1 if en_dist_p[1] > self.gamer_pos[1] else 0
        en_down = 1 if en_dist_p[1] < self.gamer_pos[1] else 0
        en_left = 1 if en_dist_p[0] < self.gamer_pos[1] else 0
        en_right = 1 if en_dist_p[0] < self.gamer_pos[1] else 0
        data.append(en_dist_h/50)
        data.append(en_up)
        data.append(en_down)
        data.append(en_left)
        data.append(en_right)

        if len(self.keys_pos) > 1:
            key_dist = [self.pif_dist(i, self.gamer_pos) for i in self.keys_pos]
            lst_num = list(enumerate(key_dist, 0))
            key_dist_h = min(lst_num, key=lambda i: i[1])
            key_dist_p = self.keys_pos[key_dist_h[0]]
            key_up = 1 if key_dist_p[1] > self.gamer_pos[1] else 0
            key_down = 1 if key_dist_p[1] < self.gamer_pos[1] else 0
            key_left = 1 if key_dist_p[0] < self.gamer_pos[1] else 0
            key_right = 1 if key_dist_p[0] < self.gamer_pos[1] else 0
            data.append(key_dist_h[1]/24)
            data.append(key_up)
            data.append(key_down)
            data.append(key_left)
            data.append(key_right)
        else:
            data.append(0)
            data.append(0)
            data.append(0)
            data.append(0)
            data.append(0)
        key_count = len(self.keys_pos)
        data.append(key_count)

        exit_dist = [self.pif_dist(i, self.gamer_pos) for i in self.exit_pos]
        exit_dist_h = min(exit_dist)
        exit_dist_p = self.exit_pos[exit_dist.index(exit_dist_h)]
        exit_up = 1 if exit_dist_p[1] > self.gamer_pos[1] else 0
        exit_down = 1 if exit_dist_p[1] < self.gamer_pos[1] else 0
        exit_left = 1 if exit_dist_p[0] < self.gamer_pos[1] else 0
        exit_right = 1 if exit_dist_p[0] < self.gamer_pos[1] else 0
        data.append(exit_dist_h/50 if key_count > 0 else exit_dist_h/12)
        data.append(exit_up)
        data.append(exit_down)
        data.append(exit_left)
        data.append(exit_right)

        data.append(self.is_jump)
        data.append(self.time_left/10000)
        data.append(self.lives)

        for i in range(-1, 2):
            for j in range(-2, 2):
                pos = [self.gamer_pos[0]+i, self.gamer_pos[0]+j]
                if not (i == 0 and -1 <= j <= 0):
                    if self.can_place(pos, i, j):
                        if self.map[pos[1]][pos[0]] == 6:
                            data.append(2)
                        elif self.map[pos[1]][pos[0]] in [7, 8]:
                            data.append(1)
                        elif self.map[pos[1]][pos[0]] in [1, 2, 3]:
                            data.append(self.map[pos[1]][pos[0]]+2)
                        elif self.map[pos[1]][pos[0]] == 0:
                            data.append(6)
                        else:
                            data.append(self.map[pos[1]][pos[0]]+3)
                    else:
                        data.append(0)
        return data

    def can_place(self, pos, i, j):
        if i == 0 and -1 <= j <= 0:
            return False
        if -1 < pos[1] < len(self.map) and -1 < pos[0] < len(self.map[0]):
            return True
        return False

    @staticmethod
    def pif_dist(a, b):
        dist = pow(pow(a[0]-b[0], 2)+pow(a[1]-b[1], 2), 0.5)
        return dist

    def find_on_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 4:
                    self.keys_pos.append([j, i])
                elif self.map[i][j] == 5:
                    self.exit_pos.append([j, i])
        return True


class DQN:
    def __init__(self):
        self.size = [6, 29]
        self.input = []
        self.output = [1, 2, 3, 4, 5, 6]
        self.outputScore = [0, 0, 0, 0, 0, 0]
        self.weight = [[0 for i in range(0, 6)] for j in range(len(self.input))]
        self.alpha = 0.6
        self.lastMove = -1
        self.lastInput = []
        self.move = -1
        self.g_pos = []
        self.lg_pos = []
        self.random = 0.25

    def teach_game(self, input_data, prev_input, last_move, weight, g_pos, lg_pos):
        if len(weight) > 0:
            self.weight = weight
        else:
            self.weight = [[1 for i in range(6)] for j in range(len(input_data))]
        self.g_pos = g_pos
        self.lg_pos = lg_pos
        self.lastMove = last_move
        self.lastInput = prev_input
        self.input = input_data
        self.score()
        max_score = max(self.outputScore)
        self.move = self.outputScore.index(max_score)
        if random.random() < self.random:
            self.move = random.randint(1, 6)
        if self.lastMove != -1:
            self.reward(self.lastMove-1, self.is_better())
        return self.move, self.input, self.weight

    def step_game(self, input_data, weight):
        if len(weight) > 0:
            self.weight = weight
        self.input = input_data
        self.score()
        max_score = max(self.outputScore)
        self.move = self.outputScore.index(max_score)
        return self.move, self.input, self.weight

    def is_better(self):
        sum_score = 0
        if self.move != self.lastMove:
            sum_score += 2
        if self.input[18] >= self.lastInput[18]:
            sum_score += 3
        if self.input[0] >= self.lastInput[0]:
            sum_score += 1
        if self.input[10] <= self.lastInput[10]:
            sum_score += 1
        if self.input[10] < self.lastInput[10]:
            sum_score += 3
        if self.input[10] < 1 and self.input[11] < self.lastInput[11]:
            sum_score += 3
        if self.input[5] <= self.lastInput[5]:
            sum_score += 2
        if self.input[5] < self.lastInput[5]:
            sum_score += 5
        if self.input[11] <= self.lastInput[11]:
            sum_score += 1
        if not(self.lg_pos[0] == self.g_pos[0] or self.lg_pos[1] == self.g_pos[1]):
            sum_score += 2
        if sum_score > 6:
            return True
        return False

    def reward(self, out_id, exit_result):
        if exit_result:
            for i in range(len(self.weight)):
                self.weight[i][out_id] += 1 * self.lastInput[i]
        else:
            for j in range(len(self.weight)):
                self.weight[j][out_id] -= 1 * self.lastInput[j]

    def score(self):
        for i in range(0, len(self.outputScore)):
            for j in range(0, len(self.input)):
                if j == 5:
                    self.outputScore[i] -= self.input[j] * self.weight[j][i] / 10
                elif i == 10:
                    self.outputScore[i] -= self.input[j] * self.weight[j][i] * 2
                elif i == 11:
                    self.outputScore[i] -= self.input[j] * self.weight[j][i] / 20
                elif i == 18:
                    self.outputScore[i] += self.input[j] * self.weight[j][i] * 3
                else:
                    self.outputScore[i] += self.input[j] * self.weight[j][i]
            self.outputScore[i] += self.future_score(self.outputScore[i])

    def future_score(self, score):
        sum_arr = 0
        for i in range(1, 4):
            sum_arr += score*(pow(self.alpha, i))
        return sum_arr

    def print_size(self):
        print(len(self.input), len(self.output), len(self.weight), len(self.weight[0]))
