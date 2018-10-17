import csv
import pickle
import numpy as np


def calVar(data_set):
    return np.var(data_set[:, -1])


def splitSet(data_set, feat, feat_val):
    left_data = data_set[np.nonzero(data_set[:, feat] > feat_val)[0], :]
    right_data = data_set[np.nonzero(data_set[:, feat] <= feat_val)[0], :]
    return left_data, right_data


def chooseFeat(data_set, args=(1, 4)):
    # 停止条件1：数据集中所有数据类别相同
    if len(set(data_set[:, -1].T.tolist()[0])) == 1:
        print("All the same")
        return None, np.mean(data_set[:, -1])

    init_var = calVar(data_set)
    best_feat = -1
    best_val = 0
    min_val = np.inf

    m, n = data_set.shape
    for feat in range(n-1):
        for val in set(data_set[:, feat].T.tolist()[0]):
            left_data, right_data = splitSet(data_set, feat, val)
            # 左子树或右子树中样本过少
            if left_data.shape[0] < args[1] or right_data.shape[0] < args[1]:
                continue
            current_val = (calVar(left_data) * left_data.shape[0] + calVar(right_data) * right_data.shape[0]) / data_set.shape[0]
            if current_val < min_val:
                min_val = current_val
                best_feat = feat
                best_val = val

    # 停止条件2：划分数据集后方差差别不大
    if init_var - min_val < args[0]:
        return None, np.mean(data_set[:, -1])

    left_data, right_data = splitSet(data_set, best_feat, best_val)
    # 停止条件3：左子树或右子树中样本过少
    if left_data.shape[0] < args[1] or right_data.shape[0] < args[1]:
        print("Sample too few")
        return None, np.mean(data_set[:, -1])

    return best_feat, best_val


def buildTree(data_set, args):
    best_feat, best_val = chooseFeat(data_set, args)
    if best_feat == None:
        return best_val
    dt = {}
    dt['splitFeat'] = best_feat
    dt['splitVal'] = best_val
    left_data, right_data = splitSet(data_set, best_feat, best_val)
    dt['left'] = buildTree(left_data, args)
    dt['right'] = buildTree(right_data, args)
    return dt


def isLeaf(dt):
    return type(dt).__name__!='dict'


def leafMean(dt):
    if not isLeaf(dt['left']):
        dt['left'] = leafMean(dt['left'])
    if not isLeaf(dt['right']):
        dt['right'] = leafMean(dt['right'])
    return (dt['left'] + dt['right']) / 2.0


def postPrune(dt, data_set):
    if data_set.shape[0] == 0:
        return leafMean(dt)
    if not isLeaf(dt['left']) or not isLeaf(dt['right']):
        left_data, right_data = splitSet(data_set, dt['splitFeat'], dt['splitVal'])
        if not isLeaf(dt['left']):
            dt['left'] = postPrune(dt['left'], left_data)
        if not isLeaf(dt['right']):
            dt['right'] = postPrune(dt['right'], right_data)
    if isLeaf(dt['left']) and isLeaf(dt['right']):
        left_data, right_data = splitSet(data_set, dt['splitFeat'], dt['splitVal'])
        err_without_merge = (np.sum(np.power(left_data[:, -1] - dt['left'], 2)) + np.sum(np.power(right_data[:, -1] - dt['right'], 2)))
        leaf_mean = leafMean(dt)
        err_with_merge = np.sum(np.power(data_set[:, -1] - leaf_mean, 2))
        if err_with_merge > err_without_merge:
            print("Leaf Merged.")
            return leaf_mean
        else:
            return dt
    else:
        return dt


def predData(dt, test_data):
    if isLeaf(dt):
        return float(dt)
    if test_data[0, dt['splitFeat']] > dt['splitVal']:
        return predData(dt['left'], test_data)
    else:
        return predData(dt['right'], test_data)


def predSet(dt, test_set):
    m = test_set.shape[0]
    y_hat = np.zeros((1, m))
    y_hat = np.mat(y_hat)
    for i in range(m):
        y_hat[0, i] = predData(dt, test_set[i])
    return y_hat


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


def splitData(data_set, split_rate):
    split_idx = int(len(data_set) * split_rate)
    train_set, valid_set = data_set[:split_idx], data_set[split_idx:]
    return train_set, valid_set


def findDepth(dt):
    if isLeaf(dt):
        return 0
    else:
        return max(findDepth(dt['left']), findDepth(dt['right'])) + 1


data_set = readData("../DATA/train.csv", 0)
train_set, valid_set = splitData(data_set, 0.8)
valid_x = [valid_set[i][:-1] for i in range(len(valid_set))]
valid_y = [valid_set[i][-1] for i in range(len(valid_set))]
train_set = np.mat(train_set)

args = (0.01, 100)

# dt = buildTree(train_set, args)
# dt_file = open("dt-" + str(args[0]) + "-" + str(args[1]) + "-no-prune.bin", "wb")
# dt_file.write(pickle.dumps(dt))
# dt_file.close()

dt_file = open("dt-" + str(args[0]) + "-" + str(args[1]) + "-no-prune.bin", "rb")
dt = pickle.loads(dt_file.read())
dt_file.close()

print("Depth:\t", findDepth(dt))
valid_x = np.mat(valid_x)
valid_y_hat = predSet(dt, valid_x)
valid_y = np.mat(valid_y)
print(np.corrcoef(valid_y, valid_y_hat)[0][1])
test_set = readData("../DATA/testStudent.csv", 1)
test_x = np.mat(test_set)
test_y_hat = predSet(dt, test_x)
test_y_hat = [test_y_hat[0, i] for i in range(test_y_hat.shape[1])]
print(len(test_y_hat))
file = open("CART-REG-" + str(args[0]) + "-" + str(args[1]) + "-no-prune.txt", "w", encoding="utf-8")
for data in test_y_hat:
    file.write(str(data) + '\n')
file.close()
