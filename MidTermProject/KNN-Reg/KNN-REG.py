# -*- coding: utf-8 -*-
import numpy as np
import csv

# 从csv文件加载训练集
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


# 提取数据
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



def splitData(data_set, split_rate):
    split_idx = int(len(data_set[0]) * split_rate)
    train_x, valid_x = data_set[0][:split_idx], data_set[0][split_idx:]
    train_y, valid_y = data_set[1][:split_idx], data_set[1][split_idx:]
    return (train_x, train_y), (valid_x, valid_y)


def validData(train_set, valid_set, k):
    train_x = train_set[0]
    train_y = train_set[1]
    train_count = len(train_x)
    valid_x = valid_set[0][:100]
    valid_y = valid_set[1][:100]
    valid_count = len(valid_x)

    for k in range(3, 13):
        pred_list = []
        for i in range(valid_count):
            dist_list = [0 for col in range(train_count)]
            for j in range(train_count):
                if np.linalg.norm(valid_x[i]) > 0:
                    dist_list[j] = np.matmul(np.matrix(valid_x[i]), np.matrix(train_x[j]).T) / (
                                np.linalg.norm(valid_x[i]) * np.linalg.norm(train_x[j]))
            if float(max(dist_list)) != 1:
                temp = 0
                count = 0
                for j in range(k):
                    if max(dist_list) <= 0:
                        break
                    index = dist_list.index(max(dist_list))
                    count += 1 * float(dist_list[index])
                    cal = float(np.float(train_y[index]) * dist_list[index])
                    temp += cal
                    dist_list[index] = -1
                temp /= count
            else:
                index = dist_list.index(max(dist_list))
                temp = train_y[index]
            # print("Real:\t", valid_y[i], "\t\tPredict:\t", temp)
            pred_list.append(temp)

        print("Corr", k, ":\t", np.corrcoef(valid_y[:valid_count], pred_list)[0][1])


def predData(train_set, test_set, k):
    train_x = train_set[0]
    train_y = train_set[1]
    train_count = len(train_x)
    test_x = test_set
    test_count = len(test_x)

    file = open("KNN-REG"+str(k)+".csv", "w", encoding="utf-8")

    for i in range(test_count):
        dist_list = [0 for col in range(train_count)]
        for j in range(train_count):
            if np.linalg.norm(test_x[i]) > 0:
                dist_list[j] = np.matmul(np.matrix(test_x[i]), np.matrix(train_x[j]).T) / (
                        np.linalg.norm(test_x[i]) * np.linalg.norm(train_x[j]))
        if float(max(dist_list)) != 1:
            temp = 0
            count = 0
            for j in range(k):
                if max(dist_list) <= 0:
                    break
                index = dist_list.index(max(dist_list))
                count += 1 * float(dist_list[index])
                cal = float(np.float(train_y[index]) * dist_list[index])
                temp += cal
                dist_list[index] = -1
            temp /= count
        else:
            index = dist_list.index(max(dist_list))
            temp = train_y[index]
        # print(temp)
        file.write(str(temp)+'\n')
    file.close()


train_set = readData("train.csv", 0)
train_set = processData(train_set, 0)
test_set = readData("testStudent.csv", 1)
test_set = processData(test_set, 1)
predData(train_set, test_set, 8)
