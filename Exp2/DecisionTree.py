import math
import collections
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


# Calculate the gini index of the data set
def calGini(data_set):
    gini = 1
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
        gini -= prob * prob

    return gini


# Calculate the performance(info gain / info gain ratio / gini gain) of chosen label
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
    elif type == 2:
        gini_gain = calGini(data_set)
        label_col = [data[label_index] for data in data_set]
        val_list = set(label_col)

        for label_val in val_list:
            sub_set = divideSet(data_set, label_index, label_val)
            prob = len(sub_set) / len(data_set)
            gini_gain -= prob * calGini(sub_set)
        return gini_gain
    else:
        raise ValueError("Type: only value 0(info gain), 1(info gain ratio), 2(gini impurity) available.")


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
def buildTree(data_set, label_list, type):
    pred_list = [data[-1] for data in data_set]
    if pred_list.count(pred_list[0]) == len(pred_list):
        return pred_list[0]

    if len(data_set) == 1:
        return pred_list[0]

    best_label_index = chooseLabel(data_set, type)
    best_label_val = label_list[best_label_index]
    decision_tree = {(best_label_index, best_label_val): {}}
    del(label_list[best_label_index])
    label_col = [data[best_label_index] for data in data_set]
    val_list = set(label_col)

    for val in val_list:
        sub_labels = label_list[:]
        decision_tree[(best_label_index, best_label_val)][val] = buildTree(divideSet(data_set, best_label_index, val), sub_labels, type)

    return decision_tree


def predRes(decision_tree, data):
    while type(decision_tree).__name__ == "dict":
        used_label = list(decision_tree.keys())[0]
        used_val = data[used_label[0]]
        if used_val in decision_tree[used_label].keys():
            decision_tree = decision_tree[used_label][used_val]
        else:
            decision_tree = decision_tree[used_label][list(decision_tree[used_label].keys())[0]]
        del data[used_label[0]]
    return decision_tree
