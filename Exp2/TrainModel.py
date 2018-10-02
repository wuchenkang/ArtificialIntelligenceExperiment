import DecisionTree
import PreProcess
# import TreePlotter


def trainModel():
    PreProcess.preProcess("car_train.csv", 5)
    data_set = PreProcess.loadData("train_set_4.csv")
    labels = [chr(ord('A')+i) for i in range(len(data_set[0])-1)]
    decision_tree = DecisionTree.buildTree(data_set, labels, 1)

    valid_all = PreProcess.loadData("valid_set_4.csv")
    valid_data = [[data[i] for i in range(len(data)-1)] for data in valid_all]
    valid_res = [data[-1]for data in valid_all]
    correct = 0
    total = 0
    for data in valid_data:
        predict = DecisionTree.predRes(decision_tree, data)
        if predict == valid_res[total]:
            correct += 1
        total += 1
    print(correct, "/", total)


trainModel()
