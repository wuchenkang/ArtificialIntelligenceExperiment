import CART_REG
import random
import multiprocessing
import numpy as np


def shuffleData(data_set, shuffle_rate):
    shuffled_data = []
    for i in range(int(len(data_set) * shuffle_rate)):
        shuffled_data.append(data_set[random.randint(0, len(data_set)-1)])
    return shuffled_data


def randomFeat(feat_count, list_size):
    feat_list = []
    for i in range(list_size):
        random_feat = random.randint(0, feat_count-1)
        while random_feat in feat_list:
            random_feat = random.randint(0, feat_count - 1)
        feat_list.append(random_feat)
    return feat_list


def extractFeat(data_set, feat_list, type):
    result_set = []
    for data in data_set:
        temp = []
        for i in range(len(feat_list)):
            temp.append(data[feat_list[i]])
        if type == 0:
            temp.append(data[-1])
        result_set.append(temp)
    return result_set


def buildForest(train_set, forest_size, shuffle_rate, feat_count, list_size, tree_args):
    random_forest = [None for _ in range(forest_size)]
    pool = multiprocessing.Pool(100)
    for i in range(forest_size):
        random_forest[i] = {}
        random_forest[i]['feat_list'] = randomFeat(feat_count, list_size)
        train_temp = shuffleData(train_set, shuffle_rate)
        train_temp = extractFeat(train_temp, random_forest[i]['feat_list'], 0)
        train_temp = np.mat(train_temp)
        random_forest[i]['tree'] = pool.apply_async(CART_REG.buildTree, args=(train_temp, tree_args,))

    pool.close()
    pool.join()
    for i in range(forest_size):
        random_forest[i]['tree'] = random_forest[i]['tree'].get()
    return random_forest


def predData(random_forest, test_x):
    pred_temp = []
    for i in range(len(random_forest)):
        test_temp = extractFeat(test_x, random_forest[i]['feat_list'], 1)
        test_temp = np.mat(test_temp)
        pred_temp.append(CART_REG.predSet(random_forest[i]['tree'], test_temp))

    pred_res = np.zeros((1, pred_temp[0].shape[1]))
    for i in range(pred_temp[0].shape[1]):
        for j in range(len(pred_temp)):
            pred_res[0, i] += pred_temp[j][0, i]
        pred_res[0, i] /= len(pred_temp)
    pred_res = np.mat(pred_res)
    return pred_res


if __name__ == "__main__":
    split_rate_ = 0.8
    data_set_ = CART_REG.readData("../DATA/train.csv", 0)
    # train_set = data_set
    train_set_, valid_set_ = CART_REG.splitData(data_set_, split_rate_)

    forest_size_ = 500
    shuffle_rate_ = 0.75
    feat_count_ = 6
    list_size_ = 3
    args_ = (0.01, 100)

    random_forest = buildForest(train_set_, forest_size_, shuffle_rate_, feat_count_, list_size_, args_)

    valid_x = [valid_set_[i][:-1] for i in range(len(valid_set_))]
    valid_y = [valid_set_[i][-1] for i in range(len(valid_set_))]
    valid_y = np.mat(valid_y)
    valid_y_hat = predData(random_forest, valid_x)
    print(np.corrcoef(valid_y, valid_y_hat)[0][1])

    test_set = CART_REG.readData("../DATA/testStudent.csv", 1)
    test_y_hat = predData(random_forest, test_set)
    test_y_hat = [test_y_hat[0, i] for i in range(test_y_hat.shape[1])]
    print(test_y_hat[:20])
    print(len(test_y_hat))
    # file = open("store/predict/RF-REG-" + str(args_[0]) + "-" + str(args_[1]) + "-" + str(split_rate_) + "-no-prune.txt", "w", encoding="utf-8")
    # file = open("store/predict/RF-REG-" + str(args_[0]) + "-" + str(args_[1]) + "-no-valid-" + "-no-prune.txt", "w", encoding="utf-8")
    # for data in test_y_hat:
    #     file.write(str(data) + '\n')
    # file.close()
