import csv
import math
import time


def main():
    print("Start!")
    t = time.time()

    # Read sentences from file and store them as list of words
    file = open("semeval.txt")
    word_list = []
    sentence_list = []
    sentence_count = 0
    for line in file:
        words = line.split("\t")[2].strip().split(" ")
        sentence_list.append(words)
        for word in words:
            if word not in word_list:
                word_list.append(word)
        sentence_count += 1
    file.close()

    word_count = len(word_list)
    TF = [[0 for col in range(word_count)] for row in range(sentence_count)]
    IDF = [0 for col in range(word_count)]
    TF_IDF = [[0 for col in range(word_count)] for row in range(sentence_count)]

    # Store the index of words in word_list
    index = dict()
    for i in range(word_count):
        index[word_list[i]] = i

    # For every word in a sentence, add the position where it is recorded in TF matrix by one
    for i in range(sentence_count):
        words = sentence_list[i]
        for word in words:
            TF[i][index[word]] += 1

    # Normalization TF and count for IDF
    for i in range(sentence_count):
        for j in range(word_count):
            if TF[i][j] > 0:
                TF[i][j] /= len(sentence_list[i])
                IDF[j] += 1

    # Calculate IDF by word frequency in sentences
    for i in range(word_count):
        IDF[i] = math.log(sentence_count / (1 + IDF[i]))

    # Calculate TF-IDF by multiple TF and IDF
    for i in range(sentence_count):
        for j in range(word_count):
            if TF[i][j] != 0:
                TF_IDF[i][j] = TF[i][j] * IDF[j]
    print("Calculate Time:\t", time.time() - t, "s")
    t = time.time()

    # Write into the file
    file = open("16337247_WuChenkang_TFIDF.txt", "w")
    for i in range(sentence_count):
        flag = False
        for j in range(word_count):
            if TF_IDF[i][j] != 0:
                if flag:
                    file.write("\t")
                else:
                    flag = True
                file.write(str(TF_IDF[i][j]))
        file.write("\n")
    file.close()

    print("Write File Time:\t", time.time() - t, "s")
    print("Finished!")


main()

