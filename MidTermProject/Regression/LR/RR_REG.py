import csv
import numpy as np


# 数据读入
def readData(file_name, type):
    data_set = []
    data_file = open(file_name, "r", encoding="utf-8")
    data_csv = csv.reader(data_file)
    for row in data_csv:
        if type == 0:
            data_set.append([1] + row[:-2] + row[-1:])
        else:
            data_set.append([1] + row[:-1])
    data_file.close()
    data_set = data_set[1:]

    for row in data_set:
        for col in range(len(row)):
            row[col] = float(row[col])
    return data_set


# 数据处理
def processData(data_set, type):
    if type == 0:
        x = np.zeros((len(data_set), len(data_set[0]) - 1), dtype=float)
        for i in range(len(data_set)):
            for j in range(len(data_set[0]) - 1):
                x[i][j] = data_set[i][j]
    else:
        x = np.zeros((len(data_set), len(data_set[0])), dtype=float)
        for i in range(len(data_set)):
            for j in range(len(data_set[0])):
                x[i][j] = data_set[i][j]

    # 归一化
    max_x = []
    min_x = []
    data_set_inv = [[x[i][j] for i in range(len(x))] for j in range(len(x[0]))]
    for i in range(len(x[0])):
        max_x.append(max(data_set_inv[i]))
        min_x.append(min(data_set_inv[i]))
    for i in range(len(x)):
        for j in range(1, len(x[0])):
            x[i][j] = (x[i][j] - min_x[j]) * 100 / (max_x[j] - min_x[j])

    if type != 0:
        return x
    else:
        y = [data_set[i][-1] for i in range(len(data_set))]
        y = np.array(y)
        return x, y


# 数据分割
def splitData(data_set, split_rate):
    split_idx = int(len(data_set[0]) * split_rate)
    train_x, valid_x = data_set[0][:split_idx], data_set[0][split_idx:]
    train_y, valid_y = data_set[1][:split_idx], data_set[1][split_idx:]
    return (train_x, train_y), (valid_x, valid_y)


# 岭回归
def ridgeRegres(x_set, y_set, k):
    x_mat = np.mat(x_set)
    y_mat = np.mat(y_set).T
    lam = np.exp(k)
    xTx = x_mat.T * x_mat
    denom = xTx + np.eye(np.shape(x_mat)[1]) * lam
    if np.linalg.det(denom) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = denom.I * (x_mat.T * y_mat)
    return ws


# 数据预测
def predData(test_x, ws):
    test_x = np.mat(test_x)
    return np.dot(test_x, ws).T


# data_set = readData("../DATA/train.csv", 0)
# data_set = processData(data_set, 0)
# train_set, valid_set = splitData(data_set, 0.9)
# ws = ridgeRegres(train_set[0], train_set[1], -30)
# pred = predData(valid_set[0], ws)
# real = np.mat(valid_set[1])
# print("Corr:\t", np.corrcoef(pred, real)[0][1])
train_set = readData("../DATA/train.csv", 0)
train_set = processData(train_set, 0)
ws = ridgeRegres(train_set[0], train_set[1], -30)
test_x = readData("../DATA/testStudent.csv", 1)
test_x = processData(test_x, 1)
test_y = predData(test_x, ws)
test_y = [test_y[0, i] for i in range(test_y.shape[1])]
file = open("RR-REG.txt", "w", encoding="utf-8")
for data in test_y:
    file.write(str(data) + '\n')
file.close()
