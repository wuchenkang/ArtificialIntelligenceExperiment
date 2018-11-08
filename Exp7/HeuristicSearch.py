import queue


manhattan_table = None


def cal_manhattan(size):
    global manhattan_table
    manhattan_table = [[0 for _ in range(size * size)] for _ in range(size * size)]
    for i in range(size * size):
        for j in range(size * size):
            manhattan_table[i][j] = abs(i // size - j // size) + abs(i % size - j % size)


def cal_heuristic(state):
    global manhattan_table
    cost = 0
    size = state.size
    n = size * size
    for i in range(size):
        for j in range(size):
            temp = state.state[i][j]
            cost += manhattan_table[i*size+j][n-temp-1]
    return cost


class State:
    def __init__(self, size, state, pivot, cost, parent):
        if state[pivot[0]][pivot[1]] != 0:
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
        if self.size == other.size and self.state == other.state and self.pivot == other.pivot:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.size == other.size and self.eval < other.eval


def a_star(init_state):
    opened = queue.PriorityQueue()
    closed = []

    opened.put((init_state.eval, init_state))

    while not opened.empty():
        _, state = opened.get()
        closed.append(state)

        if state.heur == 0:
            ops = []
            current = state
            while current is not None:
                ops = [current.state] + ops
                current = current.parent
            return ops

        neighbors = state.get_neighbors()
        for neighbor in neighbors:
            if neighbor not in closed:
                opened.put((neighbor.eval, neighbor))
    return 'NoPath!'


if __name__ == '__main__':
    # cal_manhattan(3)
    # init_state = State(3, [[1, 2, 3], [4, 5, 6], [7, 8, 0]], (2, 2), 0, None)
    cal_manhattan(2)
    init_state = State(2, [[3,0], [1, 2]], (0,1),0, None)
    print(a_star(init_state))
