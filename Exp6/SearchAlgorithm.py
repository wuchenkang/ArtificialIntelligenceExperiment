# -*- coding: utf-8 -*-
import PreProcess
import queue


steps = 0

def DFS(data_mat, current, goal, explored):
    global steps
    steps += 1
    explored.append(current)
    # 当前节点就是目标节点，返回
    if current == goal:
        return [current]
    m = len(data_mat)
    n = len(data_mat[0])
    # 向上搜索
    if current[0]-1 >= 0 and not (current[0]-1, current[1]) in explored \
            and data_mat[current[0]-1][current[1]] != '1':
        path = DFS(data_mat, (current[0]-1, current[1]), goal, explored)
        if path is not None:
            return [current] + path
    # 向下搜索
    if current[0]+1 < m and not (current[0]+1, current[1]) in explored \
            and data_mat[current[0]+1][current[1]] != '1':
        path = DFS(data_mat, (current[0]+1, current[1]), goal, explored)
        if path is not None:
            return [current] + path
    # 向左搜索
    if current[1]-1 >= 0 and not (current[0], current[1]-1) in explored \
            and data_mat[current[0]][current[1]-1] != '1':
        path = DFS(data_mat, (current[0], current[1]-1), goal, explored)
        if path is not None:
            return [current] + path
    # 向右搜索
    if current[1]+1 < n and not (current[0], current[1]+1) in explored \
            and data_mat[current[0]][current[1]+1] != '1':
        path = DFS(data_mat, (current[0], current[1]+1), goal, explored)
        if path is not None:
            return [current] + path
    # 无到目标节点的路径，回溯
    return None


def BFS(data_mat, start, end):
    m = len(data_mat)
    n = len(data_mat[0])
    explored = []               # 被探索过的节点列表
    frontier = queue.Queue()    # 未探索的边界队列

    # 边界中加入起始节点
    frontier.put((start, []))
    explored.append(start)

    global steps
    # 当边界中仍有节点
    while not frontier.empty():
        steps += 1
        # 从边界队列头取出一个边界节点
        current, path = frontier.get()
        path = path[:] + [current]
        # 到达目标节点，返回路径
        if current == end:
            return path
        # 向上搜索
        if current[0] - 1 >= 0 and not (current[0] - 1, current[1]) in explored \
                and data_mat[current[0] - 1][current[1]] != '1':
            up = (current[0] - 1, current[1])
            frontier.put((up, path))
            explored.append(up)
        # 向下搜索
        if current[0] + 1 < m and not (current[0] + 1, current[1]) in explored \
                and data_mat[current[0] + 1][current[1]] != '1':
            down = (current[0] + 1, current[1])
            frontier.put((down, path))
            explored.append(down)
        # 向左搜索
        if current[1]-1 >= 0 and not (current[0], current[1]-1) in explored \
                and data_mat[current[0]][current[1]-1] != '1':
            left = (current[0], current[1]-1)
            frontier.put((left, path))
            explored.append(left)
        # 向右搜索
        if current[1] + 1 < n and not (current[0], current[1] + 1) in explored \
                and data_mat[current[0]][current[1] + 1] != '1':
            right = (current[0], current[1] + 1)
            frontier.put((right, path))
            explored.append(right)
    # 找不到路径，返回
    return None


def DLS(data_mat, current, goal, depth, max_depth, path):
    global steps
    steps += 1
    # 当前节点已被探索，回溯
    if current in path:
        return None
    # 超过最大深度，回溯
    if depth > max_depth:
        return None
    path = path[:] + [current]
    # 当前节点就是目标节点，返回
    if current == goal:
        return path
    m = len(data_mat)
    n = len(data_mat[0])
    # 向上搜索
    if current[0] - 1 >= 0 and data_mat[current[0] - 1][current[1]] != '1':
        up_path = DLS(data_mat, (current[0] - 1, current[1]), goal, depth+1, max_depth, path)
        if up_path is not None:
            return up_path
    # 向下搜索
    if current[0] + 1 < m and data_mat[current[0] + 1][current[1]] != '1':
        down_path = DLS(data_mat, (current[0] + 1, current[1]), goal, depth+1, max_depth, path)
        if down_path is not None:
            return down_path
    # 向左搜索
    if current[1] - 1 >= 0 and data_mat[current[0]][current[1] - 1] != '1':
        left_path = DLS(data_mat, (current[0], current[1] - 1), goal, depth + 1, max_depth, path)
        if left_path is not None:
            return left_path
    # 向右搜索
    if current[1] + 1 < n and data_mat[current[0]][current[1] + 1] != '1':
        right_path = DLS(data_mat, (current[0], current[1] + 1), goal, depth + 1, max_depth, path)
        if right_path is not None:
            return right_path
    # 无到目标节点的路径，回溯
    return None


def IDDFS(data_mat, start, end):
    # 迷宫搜索最大深度不可能超过迷宫单元格个数
    max_depth = len(data_mat) * len(data_mat[0])
    # 迭代加深最大深度，对每次迭代使用深度受限搜索寻找到目标节点的路径
    for i in range(max_depth):
        global steps
        steps = 0
        path = DLS(data_mat, start, end, 0, i, [])
        if path is not None:
            return path
    return None


def UCS(data_mat, cost_map, start, end):
    m = len(data_mat)
    n = len(data_mat[0])
    explored = []                       # 被探索过的节点列表
    frontier = queue.PriorityQueue()    # 未探索的边界优先队列
    cost = 0                            # 记录路径代价

    # 从初始节点开始探索
    frontier.put((cost, (start, [])))
    explored.append(start)

    global steps
    while not frontier.empty():
        steps += 1
        # 每次从边界优先队列中取出路径消耗最小（优先级最高）的边界节点
        cost, state = frontier.get()
        current, path = state
        path = path[:] + [current]
        if current == end:
            return path
        # 向上搜索，以上方节点的路径消耗作为优先级插入边界队列
        if current[0] - 1 >= 0 and not (current[0] - 1, current[1]) in explored \
                and data_mat[current[0] - 1][current[1]] != '1':
            up = (current[0] - 1, current[1])
            cost_up = cost + cost_map[current][up]
            frontier.put((cost_up, (up, path)))
            explored.append(up)
        # 向下搜索，以下方节点的路径消耗作为优先级插入边界队列
        if current[0] + 1 < m and not (current[0] + 1, current[1]) in explored \
                and data_mat[current[0] + 1][current[1]] != '1':
            down = (current[0] + 1, current[1])
            cost_down = cost + cost_map[current][down]
            frontier.put((cost_down, (down, path)))
            explored.append(down)
        # 向左搜索，以左方节点的路径消耗作为优先级插入边界队列
        if current[1]-1 >= 0 and not (current[0], current[1]-1) in explored \
                and data_mat[current[0]][current[1]-1] != '1':
            left = (current[0], current[1]-1)
            cost_left = cost + cost_map[current][left]
            frontier.put((cost_left, (left, path)))
            explored.append(left)
        # 向右搜索，以右方节点的路径消耗作为优先级插入边界队列
        if current[1] + 1 < n and not (current[0], current[1] + 1) in explored \
                and data_mat[current[0]][current[1] + 1] != '1':
            right = (current[0], current[1] + 1)
            cost_right = cost + cost_map[current][right]
            frontier.put((cost_right, (right, path)))
            explored.append(right)

    # 找不到路径，返回
    return None


if __name__ == '__main__':
    data_mat = PreProcess.file_to_matrix('Data.txt')
    start, end = PreProcess.find_goal(data_mat)
    print("Maze Explore Problem")
    print("\tStart:\t", start)
    print("\tEnd:\t", end)
    print("\tSize:\t", len(data_mat), "*", len(data_mat[0]))

    steps = 0
    print("Search Algorithm:\tDFS")
    path = DFS(data_mat, start, end, [])
    if path is not None:
        print("\tPath Length:\t", len(path) - 1)
        print("\tPath:\t", path)
        print("\tSearch Steps:\t", steps)
    else:
        print("\tNo valid path found!")

    steps = 0
    print("Search Algorithm:\tBFS")
    path = BFS(data_mat, start, end)
    if path is not None:
        print("\tPath Length:\t", len(path) - 1)
        print("\tPath:\t", path)
        print("\tSearch Steps:\t", steps)
    else:
        print("\tNo valid path found!")

    steps = 0
    print("Search Algorithm:\tDLS")
    path = DLS(data_mat, start, end, 0, 200, [])
    if path is not None:
        print("\tPath Length:\t", len(path) - 1)
        print("\tPath:\t", path)
        print("\tSearch Steps:\t", steps)
    else:
        print("\tNo valid path found!")

    steps = 0
    print("Search Algorithm:\tIDDFS")
    path = IDDFS(data_mat, start, end)
    if path is not None:
        print("\tPath Length:\t", len(path) - 1)
        print("\tPath:\t", path)
        print("\tSearch Steps:\t", steps)
    else:
        print("\tNo valid path found!")

    cost_map = {}
    for i in range(len(data_mat)):
        for j in range(len(data_mat[0])):
            cost_map[(i, j)] = {}
            cost_map[(i, j)][(i - 1, j)] = 1
            cost_map[(i, j)][(i + 1, j)] = 1
            cost_map[(i, j)][(i, j - 1)] = 1
            cost_map[(i, j)][(i, j + 1)] = 1
    steps = 0
    print("Search Algorithm:\tUCS")
    path = UCS(data_mat, cost_map, start, end)
    if path is not None:
        print("\tPath Length:\t", len(path) - 1)
        print("\tPath:\t", path)
        print("\tSearch Steps:\t", steps)
    else:
        print("\tNo valid path found!")
