import csv
import time
import numpy as np


def main():
    begin = time.time()
    # Open train set file
    train_file = open("train_set.csv", "r")
    csv_file = csv.reader(train_file)
    word_list = []              # Store words that appear in sentences
    train_list = []             # Store sentences in train set
    train_count = 0             # Store number of sentences in train set
    emotion_list = []           # Store emotions in train set
    flag = False                # Used to jump the first line of the file

    # Read train set and split every sentence in it into words amd corresponding emotion
    for line in csv_file:
        if flag:
            words = line[0].split(" ")
            train_list.append(words)
            for word in words:
                if word not in word_list:
                    word_list.append(word)
            temp = []
            for i in range(6):
                temp.append(line[i + 1])
            emotion_list.append(temp)
        else:
            flag = True
    train_file.close()
    word_count = len(word_list)
    train_count = len(train_list)

    # Store the index of words in word_list
    word_index = dict()
    for i in range(word_count):
        word_index[word_list[i]] = i

    # Gather one-hot matrix for train set
    train_matrix = np.zeros((train_count, word_count))
    for i in range(train_count):
        words = train_list[i]
        for word in words:
            train_matrix[i][word_index[word]] = 1

    # # Read validation set and split every sentence in it into words
    # validation_file = open("validation_set.csv", "r")
    # csv_file = csv.reader(validation_file)
    # validation_list = []            # Store sentences in train set
    # validation_count = 0            # Store number of sentences in train set
    # flag = False
    # for line in csv_file:
    #     if flag:
    #         words = line[0].split(" ")
    #         validation_list.append(words)
    #     else:
    #         flag = True
    # validation_file.close()
    # validation_count = len(validation_list)
    #
    # # Gather one-hot matrix for validation set
    # validation_matrix = np.zeros((validation_count, word_count))
    # for i in range(validation_count):
    #     words = validation_list[i]
    #     for word in words:
    #         if word in word_list:
    #             validation_matrix[i][word_index[word]] = 1
    #
    #
    # # Store the distances between elements in validation set and train set
    # dist_list = [[0 for col in range(train_count)] for row in range(validation_count)]
    #
    # # # Calculate the accuracy rate for some possible k
    # # for k in range(1, 25):
    # # knn_list = [[] for row in range(validation_count)]  # Store KNN-Reg for elements in validation set
    # predict_list = []                                   # Store predict result for elements in validation set
    #
    # k = 20
    #
    # # Prediction
    # for i in range(validation_count):
    #     for j in range(train_count):
    #         if np.linalg.norm(validation_matrix[i]) > 0:
    #             dist_list[i][j] = np.matmul(np.matrix(validation_matrix[i]),  np.matrix(train_matrix[j]).T) / (np.linalg.norm(validation_matrix[i]) * np.linalg.norm(train_matrix[j]))
    #     if float(max(dist_list[i])) != 1:
    #         sum = 0
    #         temp = [0 for _ in range(6)]
    #         for j in range(k):
    #             if max(dist_list[i]) <= 0:
    #                 break
    #             index = dist_list[i].index(max(dist_list[i]))
    #             # knn_list[i][j] = index
    #             for e in range(6):
    #                 cal = float(np.float(emotion_list[index][e]) / dist_list[i][index])
    #                 temp[e] += cal
    #                 sum += cal
    #             dist_list[i][index] = -1
    #         if sum > 0:
    #             for e in range(6):
    #                 temp[e] /= sum
    #     else:
    #         index = dist_list[i].index(max(dist_list[i]))
    #         for e in range(6):
    #             temp[e] = emotion_list[index][e]
    #     # print(temp)
    #     predict_list.append(temp)
    #
    # # Write result into csv file
    # file = open("validation_res_reg.csv", "w", newline="")
    # csv_write = csv.writer(file, dialect="excel")
    # csv_write.writerow(["Text ID", "anger", "disgust", "fear", "joy", "sad", "surprise"])
    # for i in range(validation_count):
    #     csv_write.writerow([str(i+1), predict_list[i][0], predict_list[i][1], predict_list[i][2], predict_list[i][3], predict_list[i][4], predict_list[i][5]])
    # file.close()
    # end = time.time()
    # print(end-begin)

    # The correspording best value of p and k
    p = 2
    k = 3

    # Read test set and split every sentence in it into words
    test_file = open("test_set.csv", "r")
    csv_file = csv.reader(test_file)
    test_list = []
    test_count = 0
    flag = False
    for line in csv_file:
        if flag:
            words = line[1].split(" ")
            test_list.append(words)
            test_count += 1
        else:
            flag = True
    test_file.close()

    # Gather one-hot matrix for test set
    test_matrix = np.zeros((test_count, word_count))
    for i in range(test_count):
        words = test_list[i]
        for word in words:
            if word in word_list:
                test_matrix[i][word_index[word]] = 1

    # Store the distances between elements in test set and train set
    dist_list = [[0 for col in range(train_count)] for row in range(test_count)]
    # Store KNN-Reg for elements in validation set
    # knn_list = [[k for col in range(k)] for row in range(test_count)]
    # Store predict result for elements in validation set
    predict_list = []

    # Prediction
    for i in range(test_count):
        for j in range(train_count):
            if np.linalg.norm(test_matrix[i]) > 0:
                dist_list[i][j] = np.matmul(np.matrix(test_matrix[i]), np.matrix(train_matrix[j]).T) / (
                            np.linalg.norm(test_matrix[i]) * np.linalg.norm(train_matrix[j]))
        if float(max(dist_list[i])) != 1:
            sum = 0
            temp = [0 for _ in range(6)]
            for j in range(k):
                if max(dist_list[i]) <= 0:
                    break
                index = dist_list[i].index(max(dist_list[i]))
                # knn_list[i][j] = index
                for e in range(6):
                    cal = float(np.float(emotion_list[index][e]) / dist_list[i][index])
                    temp[e] += cal
                    sum += cal
                dist_list[i][index] = -1
            if sum > 0:
                for e in range(6):
                    temp[e] /= sum
        else:
            index = dist_list[i].index(max(dist_list[i]))
            for e in range(6):
                temp[e] = emotion_list[index][e]
        # print(temp)
        predict_list.append(temp)

    # Write result into csv file
    file = open("16337247_WuChenkang_KNN_regression.csv", "w", newline="")
    csv_write = csv.writer(file, dialect="excel")
    csv_write.writerow(["Text ID", "anger", "disgust", "fear", "joy", "sad", "surprise"])
    for i in range(test_count):
        csv_write.writerow([str(i+1), predict_list[i][0], predict_list[i][1], predict_list[i][2], predict_list[i][3], predict_list[i][4], predict_list[i][5]])
    file.close()
    end = time.time()
    print(end-begin)


main()