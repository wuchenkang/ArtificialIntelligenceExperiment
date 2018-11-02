# -*- coding: utf-8 -*-
import PreProcess
import queue


# 深度优先搜索
def DFS(data_mat, current, goal, explored):
    explored.append(current)
    if current == goal:
        return [current]
    m = len(data_mat)
    n = len(data_mat[0])
    # 向上
    if current[0]-1 >= 0 and not (current[0]-1, current[1]) in explored \
            and data_mat[current[0]-1][current[1]] != '1':
        path = DFS(data_mat, (current[0]-1, current[1]), goal, explored)
        if path is not None:
            return [current] + path
    # 向下
    if current[0]+1 < m and not (current[0]+1, current[1]) in explored \
            and data_mat[current[0]+1][current[1]] != '1':
        path = DFS(data_mat, (current[0]+1, current[1]), goal, explored)
        if path is not None:
            return [current] + path
    # 向左
    if current[1]-1 >= 0 and not (current[0], current[1]-1) in explored \
            and data_mat[current[0]][current[1]-1] != '1':
        path = DFS(data_mat, (current[0], current[1]-1), goal, explored)
        if path is not None:
            return [current] + path
    # 向右
    if current[1]+1 < n and not (current[0], current[1]+1) in explored \
            and data_mat[current[0]][current[1]+1] != '1':
        path = DFS(data_mat, (current[0], current[1]+1), goal, explored)
        if path is not None:
            return [current] + path
    return None


def BFS(data_mat, start, end):
    m = len(data_mat)
    n = len(data_mat[0])
    explored = []
    frontier = queue.Queue()

    frontier.put((start, []))
    explored.append(start)

    while not frontier.empty():
        current, path = frontier.get()
        path = path[:] + [current]
        if current == end:
            return path
        if current[0] - 1 >= 0 and not (current[0] - 1, current[1]) in explored \
                and data_mat[current[0] - 1][current[1]] != '1':
            up = (current[0] - 1, current[1])
            frontier.put((up, path))
            explored.append(up)
        if current[0] + 1 < m and not (current[0] + 1, current[1]) in explored \
                and data_mat[current[0] + 1][current[1]] != '1':
            down = (current[0] + 1, current[1])
            frontier.put((down, path))
            explored.append(down)
        if current[1]-1 >= 0 and not (current[0], current[1]-1) in explored \
                and data_mat[current[0]][current[1]-1] != '1':
            left = (current[0], current[1]-1)
            frontier.put((left, path))
            explored.append(left)
        if current[1] + 1 < n and not (current[0], current[1] + 1) in explored \
                and data_mat[current[0]][current[1] + 1] != '1':
            right = (current[0], current[1] + 1)
            frontier.put((right, path))
            explored.append(right)
    return None


def DLS(data_mat, current, goal, depth, max_depth, path):
    if current in path:
        return None
    if depth > max_depth:
        return None
    path = path[:] + [current]
    if current == goal:
        return path
    m = len(data_mat)
    n = len(data_mat[0])
    # 向上
    if current[0] - 1 >= 0 and data_mat[current[0] - 1][current[1]] != '1':
        up_path = DLS(data_mat, (current[0] - 1, current[1]), goal, depth+1, max_depth, path)
        if up_path is not None:
            return up_path
    # 向下
    if current[0] + 1 < m and data_mat[current[0] + 1][current[1]] != '1':
        down_path = DLS(data_mat, (current[0] + 1, current[1]), goal, depth+1, max_depth, path)
        if down_path is not None:
            return down_path
    # 向左
    if current[1] - 1 >= 0 and data_mat[current[0]][current[1] - 1] != '1':
        left_path = DLS(data_mat, (current[0], current[1] - 1), goal, depth + 1, max_depth, path)
        if left_path is not None:
            return left_path
    # 向右
    if current[1] + 1 < n and data_mat[current[0]][current[1] + 1] != '1':
        right_path = DLS(data_mat, (current[0], current[1] + 1), goal, depth + 1, max_depth, path)
        if right_path is not None:
            return right_path
    return None


def IDDFS(data_mat, start, end):
    max_depth = len(data_mat) * len(data_mat[0])
    for i in range(max_depth):
        path = DLS(data_mat, start, end, 0, i, [])
        if path is not None:
            return path
    return None


print("Maze Explore Problem")
data_mat = PreProcess.file_to_matrix('Data.txt')
start, end = PreProcess.find_goal(data_mat)
print("\tStart:\t", start)
print("\tEnd:\t", end)

print("Search Algorithm:\tDFS")
path = DFS(data_mat, start, end, [])
if path is not None:
    print("\tPath Length:\t", len(path) - 1)
    print("\tPath:\t", path)
else:
    print("No valid path found!")

print("Search Algorithm:\tBFS")
path = BFS(data_mat, start, end)
if path is not None:
    print("\tPath Length:\t", len(path) - 1)
    print("\tPath:\t", path)
else:
    print("No valid path found!")

print("Search Algorithm:\tDLS")
path = DLS(data_mat, start, end, 0, 70, [])
if path is not None:
    print("\tPath Length:\t", len(path) - 1)
    print("\tPath:\t", path)
else:
    print("No valid path found!")

print("Search Algorithm:\tIDDFS")
path = IDDFS(data_mat, start, end)
if path is not None:
    print("\tPath Length:\t", len(path) - 1)
    print("\tPath:\t", path)
else:
    print("No valid path found!")

