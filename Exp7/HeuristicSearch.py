import queue
import random
import sys


init = None
final = None
manhattan_table = None


def cal_manhattan(size):
    global manhattan_table
    manhattan_table = [[0 for _ in range(size * size)] for _ in range(size * size)]
    for i in range(size * size):
        for j in range(size * size):
            manhattan_table[i][j] = abs(i // size - j // size) + abs(i % size - j % size)


def cal_heuristic(current_state):
    global manhattan_table
    cost = 0
    size = current_state.size
    n = size * size
    for i in range(size):
        for j in range(size):
            temp = current_state.state[i][j]
            cost += manhattan_table[i*size+j][n-temp-1]
    return cost


class State:
    def __init__(self, size, state, pivot, cost, parent):
        if size != len(state) or size != len(state[0]) or state[pivot[0]][pivot[1]] != 0:
            raise RuntimeError('State not consistent!')

        self.size = size
        self.state = state
        self.pivot = pivot
        self.cost = cost
        self.heur = cal_heuristic(self)
        self.eval = self.cost + self.heur

        self.parent = parent

    def get_up(self):
        next_size = self.size
        next_state = [self.state[i][:] for i in range(next_size)]
        next_pivot = (self.pivot[0]-1, self.pivot[1])
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]-1][self.pivot[1]]
        next_state[self.pivot[0]-1][self.pivot[1]] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        return State(next_size, next_state, next_pivot, next_cost, self)

    def get_down(self):
        next_size = self.size
        next_state = [self.state[i][:] for i in range(next_size)]
        next_pivot = (self.pivot[0]+1, self.pivot[1])
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0] + 1][self.pivot[1]]
        next_state[self.pivot[0] + 1][self.pivot[1]] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        return State(next_size, next_state, next_pivot, next_cost, self)

    def get_left(self):
        next_size = self.size
        next_state = [self.state[i][:] for i in range(next_size)]
        next_pivot = (self.pivot[0], self.pivot[1]-1)
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]][self.pivot[1]-1]
        next_state[self.pivot[0]][self.pivot[1]-1] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        return State(next_size, next_state, next_pivot, next_cost, self)

    def get_right(self):
        next_size = self.size
        next_state = [self.state[i][:] for i in range(next_size)]
        next_pivot = (self.pivot[0], self.pivot[1]+1)
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]][self.pivot[1] + 1]
        next_state[self.pivot[0]][self.pivot[1] + 1] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        return State(next_size, next_state, next_pivot, next_cost, self)

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


def a_star(init_state, final_state):
    opened = queue.PriorityQueue()
    closed = []

    opened.put(init_state)

    while not opened.empty():
        state = opened.get()
        closed.append(state)

        if state == final_state:
            path = []
            current = state
            while current is not None:
                path = [current.state] + path
                current = current.parent
            return path

        neighbors = state.get_neighbors()
        for neighbor in neighbors:
            if neighbor not in closed:
                opened.put(neighbor)
    return None


def dls(current_state, final_state, max_eval, path):
    if current_state.eval > max_eval:
        return current_state.eval
    if current_state.state in path:
        return None
    path = path + [current_state.state]
    if current_state == final_state:
        return path
    neighbors = current_state.get_neighbors()
    min_eval = sys.maxsize
    for neighbor in neighbors:
        neighbor_path = dls(neighbor, final_state, max_eval, path)
        if isinstance(neighbor_path, list):
            return neighbor_path
        elif isinstance(neighbor_path, int):
            min_eval = min(min_eval, neighbor_path)
        else:
            continue
    if min_eval == sys.maxsize:
        return None
    else:
        return min_eval


def id_a_star(init_state, final_state):
    max_eval = init_state.eval
    while True:
        path = dls(init_state, final_state, max_eval, [])
        if isinstance(path, list):
            return path
        elif isinstance(path, int):
            max_eval = path
        else:
            return None


# if __name__ == '__main__':
#     cal_manhattan(4)
#     init = State(2, [[2, 1], [3, 0]], (1, 1), 0, None)
#     final = State(2, [[3, 2], [1, 0]], (1, 1), 0, None)
#     path = id_a_star(init, final)
#     for node in path:
#         print(node)
if __name__ == '__main__':
    cal_manhattan(4)
    s = State(4, [[15, 14, 13, 12], [11, 10, 9, 8], [7, 6, 5, 4], [3, 2, 1, 0]], (3, 3), 0, None)
    count = 0
    for i in range(120):
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
    print(count)
    print(s.state)
    # init = State(4, s.state, s.pivot, 0, None)
    init = State(4, [[10, 11, 13, 8], [15, 9, 6, 12], [3, 7, 14, 5], [2, 0, 1, 4]], (3, 1), 0, None)
    print()
    final = State(4, [[15, 14, 13, 12], [11, 10, 9, 8], [7, 6, 5, 4], [3, 2, 1, 0]], (3, 3), 0, None)
    path = a_star(init, final)
    print(len(path))
    for node in path:
        print(node)

# # [[15, 12, 8, 13], [11, 14, 2, 1], [7, 6, 5, 9], [3, 10, 0, 4]]
