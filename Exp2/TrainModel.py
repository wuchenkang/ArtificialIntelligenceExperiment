import csv
import DecisionTree
import PreProcess
# import TreePlotter


def validModel():
    k = 5
    PreProcess.preProcess("car_train.csv", k)
    print(str(k) + "-Fold Cross Validation")
    for m in range(3):
        if m == 0:
            print("ID.3 DT")
        elif m == 1:
            print("C4.5 DT")
        else:
            print("CART")
        avg_corr = 0
        for i in range(k):
            data_set = PreProcess.loadData("train_set_" + str(i) + ".csv")
            labels = [chr(ord('A') + i) for i in range(len(data_set[0]) - 1)]
            decision_tree = DecisionTree.buildTree(data_set, labels, m)

            valid_all = PreProcess.loadData("valid_set_" + str(i) + ".csv")
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
            print("Validation " + str(i + 1) + " Correct Rate:\t", round(corr * 100, 2), "%\t", correct, "/",
                  total)
        avg_corr /= k
        print("Average Correct Rate:\t", round(avg_corr * 100, 2), "%")


def trainModel():
    train_set = PreProcess.loadData("car_train.csv")
    labels = [chr(ord('A') + i) for i in range(len(train_set[0]) - 1)]
    decision_tree = DecisionTree.buildTree(train_set, labels, 1)
    dt_file = open("dt_file.txt", 'w')
    dt_file.write(str(decision_tree))
    dt_file.close()


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

    test_list = [[] for _ in range(len(pred_res))]
    for i in range(len(test_list)):
        test_list[i] = test_data[i][:]
        test_list[i].append(pred_res[i])

    test_file = open("test_res.csv", "w", newline="")
    csv_write = csv.writer(test_file, dialect="excel")
    for i in range(len(test_list)):
        csv_write.writerow(test_list[i])
    test_file.close()


trainModel()
predData()
