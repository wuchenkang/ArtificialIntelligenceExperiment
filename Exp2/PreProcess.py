import csv


# 将数据集依据K-折交叉验证划分为训练集和验证集
def kFold(data_set, k):
    result = [[[], []] for _ in range(k)]
    for i in range(k):
        for j in range(len(data_set)):
            if j % k != i:
                result[i][0].append(data_set[j][:])
            else:
                result[i][1].append(data_set[j][:])
    return result


# 存储划分出的K个验证集和K个数据集
def storeData(k_fold):
    k = len(k_fold)
    for i in range(k):
        train_file = open("train_set_" + str(k) + "_" + str(i) + ".csv", "w", newline="")
        train_csv = csv.writer(train_file)
        valid_file = open("valid_set_" + str(k) + "_" + str(i) + ".csv", "w", newline="")
        valid_csv = csv.writer(valid_file)
        train_list = k_fold[i][0]
        valid_list = k_fold[i][1]
        for j in range(len(k_fold[i][0])):
            train_csv.writerow(train_list[j])
        for j in range(len(k_fold[i][1])):
            valid_csv.writerow(valid_list[j])
        train_file.close()
        valid_file.close()


# 从csv文件加载数据集
def loadData(file_name):
    data_set = []
    data_file = open(file_name, "r", encoding="utf-8")
    data_csv = csv.reader(data_file)
    for row in data_csv:
        data_set.append(row)
    data_file.close()
    return data_set


# 对数据集进行预处理和K-折交叉验证
def preProcess(file_name, k):
    data_list = loadData(file_name)
    k_fold = kFold(data_list, k)
    storeData(k_fold)
