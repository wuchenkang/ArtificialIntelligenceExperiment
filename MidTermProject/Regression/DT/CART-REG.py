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
        return None, np.mean(data_set[:, -1])

    init_var = calVar(data_set)
    best_feat = -1
    best_val = 0
    min_val = np.inf

    m, n = data_set.shape()
    for feat in range(n-1):
        for val in set(data_set[:, feat].T.tolist()[0]):
            left_data, right_data = splitSet(data_set, feat, val)
            # 左子树或右子树中样本过少
            if left_data.shape[0] < args[1] or right_data.shape[0] < args[1]:
                continue
            current_val = (calVar(left_data) * left_data.shape[0] + calVar(right_data) * right_data.shape[0]) / data_set.shape[0]
            if current_val <min_val:
                min_val = current_val
                best_feat = feat
                best_val = val

    # 停止条件2：划分数据集后方差差别不大
    if init_var - min_val < args[0]:
        return None, np.mean(data_set[:, -1])

    left_data, right_data = splitSet(data_set, best_feat, best_val)
    # 停止条件3：左子树或右子树中样本过少
    if left_data.shape[0] < args[1] or right_data.shape[0] < args[1]:
        return None, np.mean(data_set[:, -1])

    return best_feat, best_val


def buildTree(data_set, args=(1, 4)):
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


data = [[1, 2, 3], [2, 2, 4], [3, 5, 7], [2, 7, 1]]
data = np.array(data)
print(data.shape[0])