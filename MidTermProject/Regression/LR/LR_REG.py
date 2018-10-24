import csv
import numpy as np


# 数据读入
def readData(file_name, type):
    data_set = []
    data_file = open(file_name, "r", encoding="utf-8")
    data_csv = csv.reader(data_file)
    for row in data_csv:
        if type == 0:
            data_set.append(row[:-2] + row[-1:])
        else:
            data_set.append(row[:-1])
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
        for j in range(len(x[0])):
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


# 线性回归
def trainModel(data_x, data_y, learning_rate, iterate_num):
    data_x = np.mat(data_x)
    data_y = np.mat(data_y).T
    weights = np.ones(shape=(1, data_x.shape[1]))
    baise = np.array([[1]])

    loss = float('inf')
    for num in range(iterate_num):
        result = np.dot(data_x, weights.T) + baise
        last_loss = loss
        loss = np.dot((data_y - result).T, data_y - result) / data_y.shape[0]
        if loss > last_loss:
            learning_rate = learning_rate * 0.8
            continue
        weights_gradient = -(2 / data_x.shape[0]) * np.dot((data_y - result).T, data_x)
        baise_gradient = -2 * np.dot((data_y - result).T, np.ones(shape=[data_x.shape[0], 1])) / data_x.shape[0]

        weights = weights - learning_rate * weights_gradient
        baise = baise - learning_rate * baise_gradient
        if num % 5000 == 0:
            print("Loss:\t", loss[0, 0])
    return weights, baise


# 数据预测
def predData(test_x, ws, b):
    test_x = np.mat(test_x)
    return np.dot(test_x, ws.T) + b


data_set = readData("../DATA/train.csv", 0)
data_set = processData(data_set, 0)
train_set, valid_set = splitData(data_set, 0.9)
ws, b = trainModel(train_set[0], train_set[1], 0.0001, 1000000)
pred = predData(valid_set[0], ws, b).T
real = np.mat(valid_set[1])
print("Corr:\n", np.corrcoef(pred, real)[0][1])
# np.savetxt("weight.txt", ws)
# np.savetxt("biase.txt", b)
# ws = np.mat(np.loadtxt("weight.txt"))
# b = np.mat(np.loadtxt("biase.txt"))
# test_x = readData("../DATA/testStudent.csv", 1)
# test_x = processData(test_x, 1)
# test_y = predData(test_x, ws, b)
# test_y = [test_y[i, 0] for i in range(test_y.shape[0])]
# file = open("LR-REG.txt", "w", encoding="utf-8")
# for data in test_y:
#     file.write(str(data) + '\n')
# file.close()
