# -*- coding: utf-8 -*-
import PreProcess


# 深度优先搜索
def DFS(data_mat, current, goal, visited):
    visited.append(current)
    if current == goal:
        return [current]
    m = len(data_mat)
    n = len(data_mat[0])
    # 向上
    if current[0]-1 >= 0 and not (current[0]-1, current[1]) in visited \
            and data_mat[current[0]-1][current[1]] != '1':
        path = DFS(data_mat, (current[0]-1, current[1]), goal, visited)
        if path != None:
            return [current] + path
    # 向下
    if current[0]+1 < m and not (current[0]+1, current[1]) in visited \
            and data_mat[current[0]+1][current[1]] != '1':
        path = DFS(data_mat, (current[0]+1, current[1]), goal, visited)
        if path != None:
            return [current] + path
    # 向左
    if current[1]-1 >= 0 and not (current[0], current[1]-1) in visited \
            and data_mat[current[0]][current[1]-1] != '1':
        path = DFS(data_mat, (current[0], current[1]-1), goal, visited)
        if path != None:
            return [current] + path
    # 向右
    if current[1]+1 < n and not (current[0], current[1]+1) in visited \
            and data_mat[current[0]][current[1]+1] != '1':
        path = DFS(data_mat, (current[0], current[1]+1), goal, visited)
        if path != None:
            return [current] + path
    return None


data_mat = PreProcess.file_to_matrix('Data.txt')
start, end = PreProcess.find_goal(data_mat)
path = DFS(data_mat, start, end, [])
print(len(path))
print(path)
