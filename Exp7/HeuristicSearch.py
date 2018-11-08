class State:
    def __init__(self, size, state, pivot, cost):
        self.size = size
        self.state = state
        self.pivot = pivot
        self.cost = cost

    def get_up(self):
        next_size = self.size
        next_state = self.state[:]
        next_pivot = self.pivot
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]-1][self.pivot[1]]
        next_state[self.pivot[0]-1][self.pivot[1]] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        next_pivot[0] -= 1

        return State(next_size, next_state, next_pivot, next_cost)

    def get_down(self):
        next_size = self.size
        next_state = self.state[:]
        next_pivot = self.pivot
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0] + 1][self.pivot[1]]
        next_state[self.pivot[0] + 1][self.pivot[1]] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        next_pivot[0] += 1

        return State(next_size, next_state, next_pivot, next_cost)

    def get_left(self):
        next_size = self.size
        next_state = self.state[:]
        next_pivot = self.pivot
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]][self.pivot[1]-1]
        next_state[self.pivot[0]][self.pivot[1]-1] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        next_pivot[1] -= 1

        return State(next_size, next_state, next_pivot, next_cost)

    def get_right(self):
        next_size = self.size
        next_state = self.state[:]
        next_pivot = self.pivot
        next_cost = self.cost + 1

        temp = next_state[self.pivot[0]][self.pivot[1] + 1]
        next_state[self.pivot[0]][self.pivot[1] + 1] = next_state[self.pivot[0]][self.pivot[1]]
        next_state[self.pivot[0]][self.pivot[1]] = temp

        next_pivot[1] += 1

        return State(next_size, next_state, next_pivot, next_cost)

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
