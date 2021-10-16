import math
import time
from queue import PriorityQueue


class PathCalc:

    def __init__(self, graph):
        self.x_len = len(graph[0])
        self.y_len = len(graph)
        self.graph = [graph[i].copy() for i in range(self.y_len)]
        self.start_time = 0
        self.end_time = 0
        self.time = 0
        self.used = []
        self.way = []
        self.key_count = 0
        self.max_key = 0

    def start_dfs(self, pos):
        pos_n = [pos[0], pos[1]]
        self.way = []
        self.start_time = time.time()
        self.count_k()
        self.used = [[0] * int(self.x_len) for j in range(self.y_len)]
        parents = [[0, 0] * int(self.x_len) for j in range(self.y_len)]
        while self.max_key > 0:
            self.key_count = 0
            pos_n, parents = self.step_dfs(pos_n, pos_n, parents)
            if pos_n[0] != pos[0] or pos[1] != pos_n[1]:
                h_arr = self.find_way(parents, pos, pos_n)
                self.max_key -= 1
                for j in range(1, len(h_arr)):
                    self.used[h_arr[j][1]][h_arr[j][0]] = 1
                    self.way.append(h_arr[j])
                pos = [pos_n[0], pos_n[1]]
            else:
                self.max_key = 0
        self.end_time = time.time()
        self.time = (-self.start_time+self.end_time)*1000
        # print("DFS time is " + str(self.time) + "ms")
        return self.way

    def count_k(self):
        self.max_key = 0
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                if self.graph[i][j] == 4:
                    self.max_key += 1

    def step_dfs(self, pos, new_pos, parents):
        self.used[pos[1]][pos[0]] = 1
        if self.graph[pos[1]][pos[0]] == 4:
            self.key_count += 1
            self.graph[pos[1]][pos[0]] = 0
            new_pos = [pos[0], pos[1]]
            return new_pos, parents
        elif self.key_count < 1:
            list_of_near = self.find_near(pos)
            for i in list_of_near:
                if self.key_count < 1:
                    parents[i[1]][i[0]] = pos
                    new_pos, parents = self.step_dfs(i, new_pos, parents)
        self.used[pos[1]][pos[0]] = 0
        return new_pos, parents

    def find_near(self, pos):
        list_of_near = []
        all_pos = [[pos[0] + 1, pos[1]], [pos[0], pos[1] - 1], [pos[0] - 1, pos[1]], [pos[0], pos[1] + 1]]
        for i in range(len(all_pos)-1):
                list_of_near = self.is_free([all_pos[i][0], all_pos[i][1]], False, list_of_near)
        list_of_near = self.is_free([all_pos[len(all_pos)-1][0], all_pos[len(all_pos)-1][1]], True, list_of_near)
        for i in list_of_near:
            if self.graph[i[1]][i[0]] == 4:
                list_of_near = [i]
        return list_of_near

    def is_free(self, pos, is_down, list_n):
        ok_state = [0, 4, 5, 7, 8]
        if -1 < pos[0] < self.x_len and -1 < pos[1] < self.y_len:
            if is_down:
                if self.used[pos[1]][pos[0]] == 0 and self.graph[pos[1]][pos[0]] in ok_state + [3]:
                    list_n.append(pos)
            elif self.used[pos[1]][pos[0]] == 0 and self.graph[pos[1]][pos[0]] in ok_state + [2]:
                list_n.append(pos)
        return list_n

    def find_way(self, parents, start, end):
        a = [end[0], end[1]]
        h = [a]
        count = 0
        while (a[0] != start[0] or a[1] != start[1]) and count < self.x_len * self.y_len:
            a = parents[a[1]][a[0]]
            h.append(a)
            count += 1
        h.append(start)
        h.reverse()
        return h

    def start_smpl_bfs(self, pos):
        self.way = []
        self.start_time = time.time()
        self.count_k()
        self.used = [[0] * int(self.x_len) for j in range(self.y_len)]
        pos_n = [pos[0], pos[1]]
        parents = [[0, 0] * int(self.x_len) for j in range(self.y_len)]
        self.key_count = 0
        if self.max_key > 0:
            pos_n, parents = self.step_bfs(pos_n, pos_n, [], parents, False)
            if pos_n[0] != pos[0] or pos[1] != pos_n[1]:
                self.max_key -= 1
                h_arr = self.find_way(parents, pos, pos_n)
                for j in range(1, len(h_arr)):
                    self.way.append(h_arr[j])
            else:
                self.max_key = 0
        else:
            pos_n, parents = self.step_bfs(pos_n, pos_n, [], parents, True)
            if pos_n[0] != pos[0] or pos[1] != pos_n[1]:
                h_arr = self.find_way(parents, pos, pos_n)
                for j in range(1, len(h_arr)):
                    self.way.append(h_arr[j])
        self.end_time = time.time()
        self.time = (-self.start_time + self.end_time) * 1000
        # print("BFS time is " + str(self.time) + "ms")
        return self.way

    def start_bfs(self, pos):
        self.way = []
        self.start_time = time.time()
        self.count_k()
        self.used = [[0] * int(self.x_len) for j in range(self.y_len)]
        pos_n = [pos[0], pos[1]]
        parents = [[0, 0] * int(self.x_len) for j in range(self.y_len)]
        while self.max_key > 0:
            self.key_count = 0
            pos_n, parents = self.step_bfs(pos_n, pos_n, [], parents, False)
            if pos_n[0] != pos[0] or pos[1] != pos_n[1]:
                self.max_key -= 1
                h_arr = self.find_way(parents, pos, pos_n)
                for j in range(1, len(h_arr)):
                    self.way.append(h_arr[j])
                pos = [pos_n[0], pos_n[1]]
            else:
                self.max_key = 0
        self.end_time = time.time()
        self.time = (-self.start_time + self.end_time) * 1000
        # print("BFS time is " + str(self.time) + "ms")
        return self.way

    def step_bfs(self, pos, new_pos, stack_h, parents, is_end):
        self.used[pos[1]][pos[0]] = 1
        list_of_near = self.find_near(pos)
        for p in range(len(list_of_near)):
            if list_of_near[p] not in stack_h and self.used[list_of_near[p][1]][list_of_near[p][0]] == 0:
                parents[list_of_near[p][1]][list_of_near[p][0]] = [pos[0], pos[1]]
                stack_h.append(list_of_near[p])
        if self.graph[pos[1]][pos[0]] == 4:
            self.key_count += 1
            self.graph[pos[1]][pos[0]] = 0
            new_pos = [pos[0], pos[1]]
        if self.graph[pos[1]][pos[0]] == 5 and is_end:
            new_pos = [pos[0], pos[1]]
        else:
            if self.key_count < 1 and len(stack_h) > 0:
                h_pos = stack_h.pop(0)
                new_pos, parents = self.step_bfs(h_pos, new_pos, stack_h, parents, is_end)
        self.used[pos[1]][pos[0]] = 0
        return new_pos, parents

    def start_uniform_cost_search(self, pos):
        self.way = []
        self.start_time = time.time()
        self.count_k()
        self.used = [[0] * int(self.x_len) for j in range(self.y_len)]
        parents = [[0, 0] * int(self.x_len) for j in range(self.y_len)]
        dist = [[0] * int(self.x_len) for j in range(self.y_len)]
        pos_n = [pos[0], pos[1]]
        while self.max_key > 0:
            self.key_count = 0
            pos_n, parents = self.step_ucs(pos_n, pos_n, PriorityQueue(), parents, dist)
            if pos_n[0] != pos[0] or pos[1] != pos_n[1]:
                self.max_key -= 1
                h_arr = self.find_way(parents, pos, pos_n)
                for j in range(1, len(h_arr)):
                    self.way.append(h_arr[j])
                pos = [pos_n[0], pos_n[1]]
            else:
                self.max_key = 0
        self.end_time = time.time()
        self.time = (-self.start_time + self.end_time) * 1000
        # print("UCS time is " + str(self.time) + "ms")
        return self.way

    def step_ucs(self, pos, new_pos, stack_h, parents, dist):
        used_h = [[0] * int(self.x_len) for j in range(self.y_len)]
        used_h[pos[1]][pos[0]] = 1

        dist[pos[1]][pos[0]] = 0
        stack_h.put((dist[pos[1]][pos[0]], pos))
        while not stack_h.empty():
            h_pos = (stack_h.get())[1]
            list_of_near = self.find_near(h_pos)
            if self.graph[h_pos[1]][h_pos[0]] == 4:
                self.key_count += 1
                self.graph[h_pos[1]][h_pos[0]] = 0
                new_pos = [h_pos[0], h_pos[1]]
                return new_pos, parents
            else:
                for el in list_of_near:
                    h_dist = dist[h_pos[1]][h_pos[0]] + 1
                    if used_h[el[1]][el[0]] != 0:
                        if dist[el[1]][el[0]] > h_dist:
                            parents[el[1]][el[0]] = [h_pos[0], h_pos[1]]
                            dist[el[1]][el[0]] = h_dist
                            stack_h, dist = self.retouch_dist(stack_h, el, dist)
                    else:
                        parents[el[1]][el[0]] = [h_pos[0], h_pos[1]]
                        dist[el[1]][el[0]] = h_dist
                        stack_h.put((dist[el[1]][el[0]], el))
                        used_h[el[1]][el[0]] = 1
        return new_pos, parents

    def start_a_star(self, pos, ch_pos):
        self.way = []
        self.start_time = time.time()
        self.count_k()
        self.used = [[0] * int(self.x_len) for j in range(self.y_len)]
        parents = [[0, 0] * int(self.x_len) for j in range(self.y_len)]
        dist = [[0] * int(self.x_len) for j in range(self.y_len)]
        pos_n = [pos[0], pos[1]]
        pos_n, parents = self.step_a_star(pos_n, pos_n, PriorityQueue(), parents, dist, ch_pos)
        if pos_n[0] != pos[0] or pos[1] != pos_n[1]:
            self.max_key -= 1
            h_arr = self.find_way(parents, pos, pos_n)
            for j in range(1, len(h_arr)):
                self.way.append(h_arr[j])
        self.end_time = time.time()
        self.time = (-self.start_time + self.end_time) * 1000
        # print("A* time is " + str(self.time) + "ms")
        return self.way

    def step_a_star(self, pos, new_pos, stack_h, parents, dist, ch_pos):
        used_h = [[0] * int(self.x_len) for j in range(self.y_len)]
        if len(used_h) < pos[1] < 0 or len(used_h[pos[1]]) < pos[0] < 0:
            return new_pos, parents
        used_h[pos[1]][pos[0]] = 1

        dist[pos[1]][pos[0]] = 0
        stack_h.put((dist[pos[1]][pos[0]], pos))
        while not stack_h.empty():
            h_pos = (stack_h.get())[1]
            list_of_near = self.find_near(h_pos)
            if h_pos[1] == ch_pos[1] and h_pos[0] == ch_pos[0]:
                self.graph[h_pos[1]][h_pos[0]] = 0
                new_pos = [h_pos[0], h_pos[1]]
                return new_pos, parents
            else:
                for el in list_of_near:
                    h_dist = dist[h_pos[1]][h_pos[0]] + self.calc_way(ch_pos, el) + 1
                    if used_h[el[1]][el[0]] != 0:
                        if dist[el[1]][el[0]] > h_dist:
                            parents[el[1]][el[0]] = [h_pos[0], h_pos[1]]
                            dist[el[1]][el[0]] = h_dist
                            stack_h, dist = self.retouch_dist(stack_h, el, dist)
                    else:
                        parents[el[1]][el[0]] = [h_pos[0], h_pos[1]]
                        dist[el[1]][el[0]] = h_dist
                        stack_h.put((dist[el[1]][el[0]], el))
                        used_h[el[1]][el[0]] = 1
        return new_pos, parents

    @staticmethod
    def calc_way(ch_pos, el):
        return int(math.sqrt((ch_pos[0]-el[0])**2 + (ch_pos[1]-el[1])**2))

    @staticmethod
    def retouch_dist(stack_h, pos, dist):
        el = stack_h.get()
        h_list = [el]
        while not stack_h.empty() and (el[1] != pos[1] or el[0] != pos[0]):
            el = stack_h.get()
            h_list.append(el)
        stack_h.put((dist[pos[1]][pos[0]], pos))
        for el in h_list:
            stack_h.put((dist[el[1]][el[0]], el))
        return stack_h, dist

# 0 - left, 1 - right, 2 - jump, 3 - not move
    class minimaxTree:
        def __init__(self):
            self.max_dep = 5
            self.cur_dep = 0
            self.position = 0
            self.score = None
            self.parent = None
            self.child = []
            self.all_way = []

        def setStartData(self, new_dep, pos, parent):
            self.cur_dep = new_dep
            self.position = pos
            self.parent = parent

    def minimaxCalc(self, pos, all_en):
        first_node = self.minimaxTree()
        self.minimax(first_node)
        first_node.all_way.reverse()
        print(first_node.all_way)

    @staticmethod
    def is_terminal_node(node):
        # чисто чекнуть чи всі ключіі є і чи на виході вже
        # якщо це термінальне, бо смерть, то 2ийпараметр - фолс
        return False, True

    def minimax(self, new_node):
        if new_node.parent is not None:
            new_node.all_way = new_node.parent.all_way.copy()
        new_node.all_way.append(new_node.position)
        isTerminal, isWin = self.is_terminal_node(new_node)
        if isTerminal:
            new_node.score = 500
            # тут треба написать таке, щоб воно рахувало оцінку відносного того, де вороги будуть, де чел буде і коли
        if new_node.cur_dep == new_node.cur_dep:
            new_node.score = 100
            # тут треба написать таке, щоб воно рахувало оцінку відносного того, де вороги будуть, де чел буде і коли
            # і не забудь що час в залежності від довжини "шляху"
            # тобто грати в гру без показу цього
            # костиль: не обновлять екран, але пройтись грою по ньому, а потім повернути все до записаного значення
            # дописати алг на тему розуміння термінальних станів
        for i in range(0, 4):
            child_node = self.minimaxTree()
            child_node.setStartData(new_node.cur_dep+1, i, new_node)
            self.minimax(child_node)
        if new_node.cur_dep % 2 == 0:
            max_score = 0
            index = 0
            for el in range(len(new_node.child)):
                if new_node.child[el].score > max_score:
                    max_score = new_node.child[el].score
                    index = el
            new_node.all_way = new_node.child[index].all_way
        else:
            min_score = 100000
            index = 0
            for el in range(len(new_node.child)):
                if new_node.child[el].score < min_score:
                    min_score = new_node.child[el].score
                    index = el
            new_node.all_way = new_node.child[index].all_way
