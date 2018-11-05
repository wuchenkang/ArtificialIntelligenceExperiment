# -*- coding: utf-8 -*-
def file_to_matrix(file_name):
    file = open(file_name, 'r')
    res_mat = []
    for line in file:
        line = line.strip()
        row = []
        for char in line:
            row.append(char)
        res_mat.append(row)
    return res_mat

def find_goal(data_mat):
    start = None
    end = None
    for i in range(len(data_mat)):
        for j in range(len(data_mat[0])):
            if data_mat[i][j] == 'S':
                start = (i, j)
            elif data_mat[i][j] == 'E':
                end = (i, j)
    if start is None or end is None:
        raise RuntimeError('No start node or end node specified.')
    return start, end
