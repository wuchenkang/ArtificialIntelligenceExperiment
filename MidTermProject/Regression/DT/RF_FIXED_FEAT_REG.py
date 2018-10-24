import CART_REG
import random
import time
import multiprocessing
import pickle
import numpy as np


def shuffleData(data_set, shuffle_rate):
    shuffled_data = []
    for i in range(int(len(data_set) * shuffle_rate)):
        shuffled_data.append(data_set[random.randint(0, len(data_set)-1)])
    return shuffled_data


def buildForest(train_set, forest_size, shuffle_rate, tree_args):
    random_forest = [None for _ in range(forest_size)]
    pool = multiprocessing.Pool()
    for i in range(forest_size):
        train_temp = shuffleData(train_set, shuffle_rate)
        train_temp = np.mat(train_temp)
        random_forest[i] = pool.apply_async(CART_REG.buildTree, args=(train_temp, tree_args,))
    pool.close()
    pool.join()
    for i in range(forest_size):
        random_forest[i] = random_forest[i].get()
    return random_forest


def predData(random_forest, test_x):
    pred_temp = []
    pool = multiprocessing.Pool()
    for i in range(len(random_forest)):
        pred_temp.append(pool.apply_async(CART_REG.predSet, args=(random_forest[i], test_x)))
    for i in range(len(random_forest)):
        pred_temp[i] = pred_temp[i].get()
    pred_res = np.zeros((1, pred_temp[0].shape[1]))
    for i in range(pred_temp[0].shape[1]):
        for j in range(len(pred_temp)):
            pred_res[0, i] += pred_temp[j][0, i]
        pred_res[0, i] /= len(pred_temp)
    pred_res = np.mat(pred_res)
    return pred_res


if __name__ == "__main__":
    split_rate_ = 0.9
    data_set_ = CART_REG.readData("../DATA/train.csv", 0)
    # train_set_ = data_set_
    train_set_, valid_set_ = CART_REG.splitData(data_set_, split_rate_)

    forest_size_ = 100
    shuffle_rate_ = 0.75
    tree_args_ = (0.008, 81)

    # random_forest_ = buildForest(train_set_, forest_size_, shuffle_rate_, tree_args_)
    #
    # forest_file = open("store/tree/rf-" + str(tree_args_[0]) + "-" + str(tree_args_[1]) + "-" + str(split_rate_) + "-no-prune.bin", "wb")
    # # forest_file = open("store/tree/dt-" + str(tree_args_[0]) + "-" + str(tree_args_[1]) + "-no-valid-" + "-no-prune.bin", "wb")
    # forest_file.write(pickle.dumps(random_forest_))
    # forest_file.close()

    forest_file = open("store/tree/rf-" + str(tree_args_[0]) + "-" + str(tree_args_[1]) + "-" + str(split_rate_) + "-no-prune.bin", "rb")
    # forest_file = open("store/tree/dt-" + str(tree_args_[0]) + "-" + str(tree_args_[1]) + "-no-valid-" + "-no-prune.bin", "wb")
    random_forest_ = pickle.loads(forest_file.read())
    forest_file.close()

    valid_x = [valid_set_[i][:-1] for i in range(len(valid_set_))]
    valid_y = [valid_set_[i][-1] for i in range(len(valid_set_))]
    valid_x = np.mat(valid_x)
    valid_y = np.mat(valid_y)
    valid_y_hat = predData(random_forest_, valid_x)
    print(np.corrcoef(valid_y, valid_y_hat)[0][1])

    test_set = CART_REG.readData("../DATA/testStudent.csv", 1)
    test_x = np.mat(test_set)
    pred_temp = []
    test_y_hat = predData(random_forest_, test_x)
    test_y_hat = [test_y_hat[0, i] for i in range(test_y_hat.shape[1])]
    print(test_y_hat[:20])
    print(len(test_y_hat))
    file = open("store/predict/RF-REG-" + str(tree_args_[0]) + "-" + str(tree_args_[1]) + "-" + str(split_rate_) + "-no-prune" + time.strftime('-%m-%d', time.localtime(time.time())) + ".txt", "w", encoding="utf-8")
    # file = open("store/predict/RF-REG-" + str(tree_args_[0]) + "-" + str(tree_args_[1]) + "-no-valid-" + "-no-prune" + time.strftime('-%m-%d', time.localtime(time.time())) + ".txt", "w", encoding="utf-8")
    for data in test_y_hat:
        file.write(str(data) + '\n')
    file.close()
