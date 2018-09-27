import math
import TreePlotter


# Calculate the entropy of the data set
def calEntropy(data_set):
    entropy = 0
    ele_count = len(data_set)
    val_counts = {}

    for data in data_set:
        pred_res = data[-1]
        if pred_res not in val_counts.keys():
            val_counts[pred_res] = 1
        else:
            val_counts[pred_res] += 1

    for val_count in val_counts.values():
        prob = val_count / ele_count
        entropy -= prob * math.log(prob, 2)

    return entropy


# Calculate the performance(info gain / info gain ratio / gini impurity) of chosen label
def calPerf(data_set, label_index, type):
    if type == 0 or type == 1:
        info_gain = calEntropy(data_set)
        split_val = 0
        label_col = [data[label_index] for data in data_set]
        val_list = set(label_col)
        for label_val in val_list:
            sub_set = divideSet(data_set, label_index, label_val)
            prob = len(sub_set) / len(data_set)
            info_gain -= prob * calEntropy(sub_set)
            split_val -= prob * math.log(prob, 2)
        info_gain_ratio = info_gain / split_val
        return (info_gain, info_gain_ratio)[type]
    else:
        # TODO - Calculate gini impurity
        pass


# Divide the data set by specific label
def divideSet(data_set, label_index, label_val):
    sub_set = []
    for data in data_set:
        if data[label_index] == label_val:
            sub_data = data[:label_index] + data[label_index+1:]
            sub_set.append(sub_data)
    return sub_set


# Choose the label with the best performance
def chooseLabel(data_set, type):
    label_num = len(data_set[0]) - 1
    best_perf = 0
    best_label = -1
    for label_index in range(label_num):
        current_perf = calPerf(data_set, label_index, type)
        if current_perf > best_perf:
            best_perf = current_perf
            best_label = label_index

    return best_label


# Build decision tree
def buildTree(data_set, label_list):
    # TODO - Build decision tree
    pass

