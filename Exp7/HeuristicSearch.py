import queue
import random
import math
import sys


manhattan_table = None
chebyshev_table = None
euclidean_table = None
difference_table = None


# 曼哈顿距离表
def cal_manhattan(size):
    global manhattan_table
    manhattan_table = [[0 for _ in range(size * size)] for _ in range(size * size)]
    for i in range(size * size):
        for j in range(size * size):
            manhattan_table[i][j] = abs(i // size - j // size) + abs(i % size - j % size)


# 切比雪夫距离表
def cal_chebyshev(size):
    global chebyshev_table
    chebyshev_table = [[0 for _ in range(size * size)] for _ in range(size * size)]
    for i in range(size * size):
        for j in range(size * size):
            chebyshev_table[i][j] = max(abs(i // size - j // size), abs(i % size - j % size))


# 欧式距离表
def cal_euclidean(size):
    global euclidean_table
    euclidean_table = [[0 for _ in range(size * size)] for _ in range(size * size)]
    for i in range(size * size):
        for j in range(size * size):
            euclidean_table[i][j] = math.sqrt((i // size - j // size)**2 + (i % size - j % size)**2)


# 匹配情况表
def cal_difference(size):
    global difference_table
    difference_table = [[0 for _ in range(size * size)] for _ in range(size * size)]
    for i in range(size * size):
        for j in range(size * size):
            if i != j:
                difference_table[i][j] = 1


# 计算当前状态对应的启发式函数值
def cal_heuristic(current_state, type):
    global manhattan_table
    global chebyshev_table
    global euclidean_table
    global difference_table
    cost = 0
    size = current_state.size
    n = size * size
    if type == 0:
        table = chebyshev_table
    elif type == 1:
        table = manhattan_table
    elif type == 2:
        table = euclidean_table
    elif type == -1:
        table = difference_table
    else:
        raise RuntimeError('Invalid parameter - type！')
    for i in range(size):
        for j in range(size):
            temp = current_state.state[i][j]
            if temp == 0:
                continue
            cost += table[i*size+j][n-temp-1]
    return cost


# 状态表示类
class State:
    def __init__(self, size, state, pivot, cost, type, parent):
        if size != len(state) or size != len(state[0]) or state[pivot[0]][pivot[1]] != 0:
            raise RuntimeError('State not consistent!')

        self.size = size                        # Puzzle大小
        self.state = state                      # 当前状态存储
        self.pivot = pivot                      # 记录'0'的位置
        self.cost = cost                        # 路径消耗值
        self.type = type                        # 启发式函数种类
        self.heur = cal_heuristic(self, type)   # 启发式函数值
        self.eval = self.cost + self.heur       # 评估函数值

        self.parent = parent                    # 父节点引用

    def get_up(self):
        next_size = self.size
        next_state = [self.state[i][:] for i in range(next_size)]
        next_pivot = (self.pivot[0]-1, self.pivot[1])
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]-1][self.pivot[1]]
        next_state[self.pivot[0]-1][self.pivot[1]] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        return State(next_size, next_state, next_pivot, next_cost, self.type, self)

    def get_down(self):
        next_size = self.size
        next_state = [self.state[i][:] for i in range(next_size)]
        next_pivot = (self.pivot[0]+1, self.pivot[1])
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0] + 1][self.pivot[1]]
        next_state[self.pivot[0] + 1][self.pivot[1]] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        return State(next_size, next_state, next_pivot, next_cost, self.type, self)

    def get_left(self):
        next_size = self.size
        next_state = [self.state[i][:] for i in range(next_size)]
        next_pivot = (self.pivot[0], self.pivot[1]-1)
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]][self.pivot[1]-1]
        next_state[self.pivot[0]][self.pivot[1]-1] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        return State(next_size, next_state, next_pivot, next_cost, self.type, self)

    def get_right(self):
        next_size = self.size
        next_state = [self.state[i][:] for i in range(next_size)]
        next_pivot = (self.pivot[0], self.pivot[1]+1)
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]][self.pivot[1] + 1]
        next_state[self.pivot[0]][self.pivot[1] + 1] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        return State(next_size, next_state, next_pivot, next_cost, self.type, self)

    def get_neighbors(self):
        neighbors = []
        if self.pivot[0] > 0:
            neighbors.append(self.get_up())
        if self.pivot[0]+1 < self.size:
            neighbors.append(self.get_down())
        if self.pivot[1] > 0:
            neighbors.append(self.get_left())
        if self.pivot[1]+1 < self.size:
            neighbors.append(self.get_right())
        return neighbors

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.size == other.size and self.eval < other.eval


# A*搜索搜索
def a_star(init_state, final_state):
    opened = queue.PriorityQueue()  # 开启列表
    closed = []                     # 关闭列表

    opened.put(init_state)          # 初始节点加入开启列表

    # 重复循环直到开启列表为空
    while not opened.empty():
        state = opened.get()        # 从开启列表中获取评价函数f(n)最小的节点n
        closed.append(state)        # 将其加入关闭列表

        # 若当前节点就是最终节点，返回从初始节点到当前节点的路径
        if state == final_state:
            path = []
            current = state
            while current is not None:
                path = [current] + path
                current = current.parent
            return path

        # 将当前节点所有不在关闭列表中的邻节点加入开启列表
        neighbors = state.get_neighbors()
        for neighbor in neighbors:
            if neighbor not in closed:
                opened.put(neighbor)

    # 开启列表为空，找不到路径
    return None


# 特殊的深度受限搜索
def dls(current_state, final_state, bound, path):
    # 估价函数达到阈值，剪枝，返回目前超过阈值的估价函数
    if current_state.eval > bound:
        return current_state.eval
    # 节点被路径检测剪枝
    if current_state in path:
        return None
    # 路径中加入当前节点
    path = path + [current_state]
    # 当前节点就是目标节点，返回路径
    if current_state == final_state:
        return path
    # 对于当前节点的所有邻节点，执行深度优先搜索
    neighbors = current_state.get_neighbors()
    min_eval = sys.maxsize
    for neighbor in neighbors:
        neighbor_path = dls(neighbor, final_state, bound, path)
        # 邻节点的深度优先搜索返回路径，说明搜索完成，返回路径
        if isinstance(neighbor_path, list):
            return neighbor_path
        # 邻节点的深度优先搜索返回估价函数值，更新超过阈值的最小估价函数值
        elif isinstance(neighbor_path, int) or isinstance(neighbor_path, float):
            min_eval = min(min_eval, neighbor_path)
        # 邻节点的深度优先搜索返回None，对应路径不存在
        else:
            continue
    # 若未更新超过阈值的最小估价函数值，说明邻节点均返回None，对应路径不存在
    if min_eval == sys.maxsize:
        return None
    # 否则返回超过阈值的最小估价函数值供IDA*使用
    else:
        return min_eval


# IDA*搜索算法
def id_a_star(init_state, final_state):
    bound = init_state.eval
    while True:
        path = dls(init_state, final_state, bound, [])
        # 找到最佳路径，返回该最佳路径
        if isinstance(path, list):
            return path
        # 返回大于当前阈值的最小估价函数值，以此更新DLS阈值
        elif isinstance(path, int) or isinstance(path, float):
            bound = path
        # 找不到路径
        else:
            return None


def print_state(state_obj):
    for i in range(len(state_obj.state)):
        print('+---+---+---+---+')
        for j in range(len(state_obj.state[0])):
            print('|', '{:2}'.format(str(state_obj.state[i][j])), end='')
        print('|')
    print('+---+---+---+---+')


def print_path(path):
    for i in range(len(path)-1):
        print(' {:2}'.format(str(path[i+1].state[path[i].pivot[0]][path[i].pivot[1]])), end='')
        if i % 6 == 5:
            print()
    if(len(path) - 1 % 6 != 0):
        print()

if __name__ == '__main__':
    cal_manhattan(4)
    cal_chebyshev(4)
    cal_euclidean(4)
    cal_difference(4)
    s = State(4, [[15, 14, 13, 12], [11, 10, 9, 8], [7, 6, 5, 4], [3, 2, 1, 0]], (3, 3), 0, 1, None)
    count = 0
    for i in range(100):
        t = random.randint(0, 3)
        if t == 0 and s.pivot[0] > 0:
            s = s.get_up()
            count += 1
        elif t == 1 and s.pivot[0] < s.size - 1:
            s = s.get_down()
            count += 1
        elif t == 2 and s.pivot[1] > 0:
            s = s.get_left()
            count += 1
        elif t == 3 and s.pivot[1] < s.size - 1:
            s = s.get_right()
            count += 1
    print('Random shuffle with ', count, 'moves.')

    init = State(4, s.state, s.pivot, 0, 1, None)
    final = State(4, [[15, 14, 13, 12], [11, 10, 9, 8], [7, 6, 5, 4], [3, 2, 1, 0]], (3, 3), 0, 1, None)

    print('Initial State：')
    print_state(init)
    print()

    print('Use manhattan distance as heuristic function.\n')

    path = a_star(init, final)
    print('Solution by A* with ', len(path) - 1, ' moves')
    print_path(path)
    print()

    path = id_a_star(init, final)
    print('Solution by IDA* with ', len(path) - 1, ' moves')
    print_path(path)

# # [[15, 12, 8, 13], [11, 14, 2, 1], [7, 6, 5, 9], [3, 10, 0, 4]]
