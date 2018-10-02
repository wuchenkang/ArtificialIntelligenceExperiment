import csv


def getData(data_file):
    data_list = []
    data_file = open(data_file, "r")
    data_csv = csv.reader(data_file)
    for row in data_csv:
        data_list.append(row)
    return data_list


def kFold(data_set, k):
    result = [[[], []] for _ in range(k)]
    for i in range(k):
        for j in range(len(data_set)):
            if j % k != i:
                result[i][0].append(data_set[j][:])
            else:
                result[i][1].append(data_set[j][:])
    return result


def storeData(k_fold):
    k = len(k_fold)
    for i in range(k):
        train_file = open("train_set_" + str(i) + ".csv", "w", newline="")
        train_csv = csv.writer(train_file)
        valid_file = open("valid_set_" + str(i) + ".csv", "w", newline="")
        valid_csv = csv.writer(valid_file)
        train_list = k_fold[i][0]
        valid_list = k_fold[i][1]
        for j in range(len(k_fold[i][0])):
            train_csv.writerow(train_list[j])
        for j in range(len(k_fold[i][1])):
            valid_csv.writerow(valid_list[j])
        train_file.close()
        valid_file.close()


def preProcess():
    data_list = getData("car_train.csv")
    k_fold = kFold(data_list, 5)
    storeData(k_fold)


preProcess()
