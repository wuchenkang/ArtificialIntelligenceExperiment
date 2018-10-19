import CART_REG
import random
import multiprocessing
import numpy as np


def shuffleData(data_set, shuffle_rate):
    shuffled_data = []
    for i in range(int(len(data_set) * shuffle_rate)):
        shuffled_data.append(data_set[random.randint(0, len(data_set)-1)])
    return shuffled_data


if __name__ == "__main__":
    split_rate = 0.8
    data_set = CART_REG.readData("../DATA/train.csv", 0)
    train_set, valid_set = CART_REG.splitData(data_set, split_rate)

    forest_size = 100
    shuffle_rate = 0.75
    args = (0.01, 100)

    random_forest = [None for _ in range(forest_size)]
    pool = multiprocessing.Pool()
    for i in range(forest_size):
        train_temp = shuffleData(train_set, shuffle_rate)
        train_temp = np.mat(train_temp)
        random_forest[i] = pool.apply_async(CART_REG.buildTree, args=(train_temp, args,))

    pool.close()
    pool.join()

    for i in range(forest_size):
        random_forest[i] = random_forest[i].get()

    valid_x = [valid_set[i][:-1] for i in range(len(valid_set))]
    valid_y = [valid_set[i][-1] for i in range(len(valid_set))]
    valid_x = np.mat(valid_x)
    valid_y = np.mat(valid_y)

    pred_temp = []
    for i in range(forest_size):
        pred_temp.append(CART_REG.predSet(random_forest[i], valid_x))

    pred_res = np.zeros((1, pred_temp[0].shape[1]))
    for i in range(pred_temp[0].shape[1]):
        for j in range(len(pred_temp)):
            pred_res[0, i] += pred_temp[j][0, i]
        pred_res[0, i] /= len(pred_temp)

    valid_y_hat = np.mat(pred_res)
    print(np.corrcoef(valid_y, valid_y_hat)[0][1])

    test_set = CART_REG.readData("../DATA/testStudent.csv", 1)
    test_x = np.mat(test_set)
    pred_temp = []
    for i in range(forest_size):
        pred_temp.append(CART_REG.predSet(random_forest[i], test_x))
    pred_res = np.zeros((1, pred_temp[0].shape[1]))
    for i in range(pred_temp[0].shape[1]):
        for j in range(len(pred_temp)):
            pred_res[0, i] += pred_temp[j][0, i]
        pred_res[0, i] /= len(pred_temp)
    test_y_hat = [pred_res[0, i] for i in range(pred_res.shape[1])]
    file = open("store/predict/RF-REG-" + str(args[0]) + "-" + str(args[1]) + "-" + str(split_rate) + "-no-prune.txt", "w", encoding="utf-8")
    # file = open("store/predict/RF-REG-" + str(args[0]) + "-" + str(args[1]) + "-no-valid-" + "-no-prune.txt", w", encoding="utf-8")
    for data in test_y_hat:
        file.write(str(data) + '\n')
    file.close()
