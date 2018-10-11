import csv
import numpy as np
import matplotlib.pyplot as plt
import DecisionTree
import PreProcess


# 对不同决策树模型进行K-折交叉验证并根据结果绘图
def validModel():
    X = np.arange(2, 17, 1)
    Y = np.zeros((3, 15))

    for m in range(3):
        # if m == 0:
        #     print("ID3")
        # elif m == 1:
        #     print("C4.5")
        # else:
        #     print("CART")
        for k in range(2, 17):
            # k = 5
            # print(str(k) + "-Fold Cross Validation")
            PreProcess.preProcess("car_train.csv", k)
            avg_corr = 0
            for i in range(k):
                data_set = PreProcess.loadData("train_set_" + str(k) + "_" + str(i) + ".csv")
                labels = [chr(ord('A') + i) for i in range(len(data_set[0]) - 1)]
                decision_tree = DecisionTree.buildTree(data_set, labels, m)

                valid_all = PreProcess.loadData("valid_set_" + str(k) + "_" + str(i) + ".csv")
                valid_data = [[data[i] for i in range(len(data) - 1)] for data in valid_all]
                valid_res = [data[-1] for data in valid_all]
                correct = 0
                total = 0
                for data in valid_data:
                    pred = DecisionTree.predRes(decision_tree, data)
                    if pred == valid_res[total]:
                        correct += 1
                    total += 1
                corr = correct / total
                avg_corr += corr
                # print("Validation " + str(i + 1) + " Correct Rate:\t", round(corr * 100, 2), "%\t", correct, "/",total)
            avg_corr /= k
            # print("Average Correct Rate:\t", round(avg_corr * 100, 2), "%\n")
            Y[m][k-2] = avg_corr
    id3 = plt.plot(X, Y[0], color='green', label='ID3')
    c45 = plt.plot(X, Y[1], color='red', label='C4.5')
    cart = plt.plot(X, Y[2], color='skyblue', label='CART')
    plt.title('Model Accuracy')
    plt.xlabel('K')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()


# 使用训练集创建决策树
def trainModel():
    train_set = PreProcess.loadData("car_train.csv")
    labels = [chr(ord('A') + i) for i in range(len(train_set[0]) - 1)]
    decision_tree = DecisionTree.buildTree(train_set, labels, 0)
    dt_file = open("dt_file.txt", 'w')
    dt_file.write(str(decision_tree))
    dt_file.close()


# 使用决策树测试集数据进行预测
def predData():
    dt_file = open("dt_file.txt", "r")
    decision_tree = eval(dt_file.read())
    dt_file.close()
    test_all = PreProcess.loadData("car_test.csv")
    test_data = [[data[i] for i in range(len(data) - 1)] for data in test_all]
    pred_res = []
    for data in test_data:
        pred = DecisionTree.predRes(decision_tree, data[:])
        pred_res.append(pred)

    # test_list = [[] for _ in range(len(pred_res))]
    # for i in range(len(test_list)):
    #     test_list[i] = test_data[i][:]
    #     test_list[i].append(pred_res[i])

    test_file = open("test_res.csv", "w", newline="")
    csv_write = csv.writer(test_file, dialect="excel")
    for i in range(len(pred_res)):
        csv_write.writerow(pred_res[i])
    test_file.close()


# validModel()
trainModel()
predData()
