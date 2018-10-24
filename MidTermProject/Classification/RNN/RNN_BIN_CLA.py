# coding:utf-8
import numpy as np
import string
import collections
import tensorflow as tf


def readData():
    # 读入数据集
    review_file =  open('trainData-2.txt', 'r', encoding='utf-8')
    reviews = review_file.read()
    review_file.close()
    label_file = open('trainLabel-2.txt', 'r', encoding='utf-8')
    labels = label_file.read()
    label_file.close()

    # 将评论集按照评论和词分割
    all_reviews = ''.join([word for word in reviews if word not in string.punctuation])
    reviews = all_reviews.split('\n')

    all_reviews = ' '.join(reviews)
    words = all_reviews.split()

    # 创建词索引
    counts = collections.Counter(words)
    vocs = sorted(counts, key=counts.get, reverse=True)
    voc_to_index = {word: i for i, word in enumerate(vocs, 1)}

    review_ints = []
    for review in reviews:
        review_ints.append([voc_to_index[word] for word in review.split()])

    labels = labels.split('\n')

    # 去除空行
    valid_idx = [i for i, review in enumerate(review_ints) if len(review) != 0]
    review_ints = [review_ints[i] for i in valid_idx]
    labels = np.array([labels[i] for i in valid_idx])

    # 将评论统一处理为250维向量，维数不够的0-padding，维数过多的截尾处理
    seq_len = 250
    feats = np.zeros((len(review_ints), seq_len), dtype=int)
    for i, row in enumerate(review_ints):
        feats[i, -len(row):] = np.array(row)[:seq_len]

    return voc_to_index, feats, labels


def splitData(feats, labels, split_rate):
    # 将数据集拆分为训练集、验证集和测试集三部分
    split_idx = int(len(feats) * split_rate)
    train_x, valid_x = feats[:split_idx], feats[split_idx:]
    train_y, valid_y = labels[:split_idx], labels[split_idx:]

    test_idx = int(len(valid_x)*0.5)
    valid_x, test_x = valid_x[:test_idx], valid_x[test_idx:]
    valid_y, test_y = valid_y[:test_idx], valid_y[test_idx:]

    return (train_x, train_y), (valid_x, valid_y), (test_x, test_y)


def get_batches(feats, labels, batch_size):
    # 将数据按批组织
    n_batches = len(feats) // batch_size
    feats, labels = feats[:n_batches * batch_size], labels[:n_batches * batch_size]
    for i in range(0, len(feats), batch_size):
        yield feats[i:i + batch_size], labels[i:i + batch_size]


class LSTMModel():
    def __init__(self, cell_size, num_layer, batch_size, learning_rate, voc_count, embedding_size):
        # 配置模型参数
        with tf.name_scope('Configuration'):
            self.cell_size = cell_size
            self.num_layer = num_layer
            self.batch_size = batch_size
            self.learning_rate = learning_rate
            self.voc_count = voc_count
            self.embedding_size = embedding_size

        # 加入输入
        with tf.name_scope('Inputs'):
            self.addInput()

        # 加入嵌入层，将一维词索引转换为二维词向量
        with tf.name_scope('EmbeddingLayer'):
            self.addEmbedding()

        # 加入LSTM网络层
        with tf.name_scope('LSTMLayer'):
            self.addLSTM()

        # 加入全连接层，将LSTM网络层结果映射到最终输出
        with tf.name_scope('Outputs'):
            self.addOutput()

        # 计算损失函数
        with tf.name_scope('Cost'):
            self.computeCost()

        # 计算准确率
        with tf.name_scope('Accuracy'):
            self.computeAccuracy()

        # 加入优化器以训练模型
        with tf.name_scope('Optimizer'):
            self.addOptimizer()

    def addInput(self):
        self.inputs = tf.placeholder(tf.int32, [None, None], name='inputs')
        self.labels = tf.placeholder(tf.int32, [None, None], name='labels')
        self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

    def addEmbedding(self):
        self.embedding = tf.Variable(tf.random_uniform((self.voc_count, self.embedding_size), -1, 1))
        self.embeded = tf.nn.embedding_lookup(self.embedding, self.inputs)

    def addLSTM(self):
        self.lstm = [tf.contrib.rnn.BasicLSTMCell(cell_size) for _ in range(num_layer)]
        self.drop = [tf.contrib.rnn.DropoutWrapper(self.lstm[i], output_keep_prob=self.keep_prob) for i in range(len(self.lstm))]
        self.cell = tf.contrib.rnn.MultiRNNCell(self.drop)
        self.initial_state = self.cell.zero_state(batch_size, tf.float32)
        self.outputs, self.final_state = tf.nn.dynamic_rnn(self.cell, self.embeded, initial_state=self.initial_state)

    def addOutput(self):
        self.predictions = tf.contrib.layers.fully_connected(self.outputs[:, -1], 1, activation_fn=tf.sigmoid)

    def computeCost(self):
        self.cost = tf.losses.mean_squared_error(self.labels, self.predictions)

    def computeAccuracy(self):
        self.correct_pred = tf.equal(tf.cast(tf.round(self.predictions), tf.int32), self.labels)
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))

    def addOptimizer(self):
        self.global_step = tf.Variable(0, trainable=False)
        self.learing_rate = tf.train.exponential_decay(self.learning_rate, self.global_step, 100, 0.95, staircase=True)
        self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.cost)


voc_to_index, feats, labels = readData()
voc_count = len(voc_to_index)
(train_x, train_y), (valid_x, valid_y), (test_x, test_y) = splitData(feats, labels, 0.8)

epochs = 10
cell_size = 128
num_layer = 2
batch_size = 500
learning_rate = 0.001
embedding_size = 300

model = LSTMModel(cell_size, num_layer, batch_size, learning_rate, voc_count, embedding_size)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
writer = tf.summary.FileWriter("logs", sess.graph)
iteration = 0
for e in range(epochs):
    state = sess.run(model.initial_state)
    for i, (x, y) in enumerate(get_batches(train_x, train_y, batch_size), 1):
        feed = {
            model.inputs: x,
            model.labels: y[:, None],
            model.keep_prob: 0.8,
            model.initial_state: state
        }
        loss, state, _ = sess.run([model.cost, model.final_state, model.optimizer], feed_dict=feed)

        if iteration % 4 == 0:
            print("Epoch: {}/{}".format(e, epochs),
                  "Iteration: {}".format(iteration),
                  "Train loss: {:.4f}".format(loss))

        if iteration % 24 == 0:
            valid_accuracy = []
            valid_state = sess.run(model.cell.zero_state(batch_size, tf.float32))
            for x, y in get_batches(valid_x, valid_y, batch_size):
                feed = {
                    model.inputs: x,
                    model.labels: y[:, None],
                    model.keep_prob: 1,
                    model.initial_state: valid_state
                }
                batch_accuracy, valid_state = sess.run([model.accuracy, model.final_state], feed_dict=feed)
                valid_accuracy.append(batch_accuracy)
            print("Val acc: {:.4f}".format(np.mean(valid_accuracy)))
        iteration += 1
saver.save(sess, "checkpoints/model.ckpt")

test_acc = []
saver.restore(sess, tf.train.latest_checkpoint('checkpoints'))
test_state = sess.run(model.cell.zero_state(batch_size, tf.float32))
for i, (x, y) in enumerate(get_batches(test_x, test_y, batch_size), 1):
    feed = {
        model.inputs: x,
        model.labels: y[:, None],
        model.keep_prob: 1,
        model.initial_state: test_state
    }
    batch_accuracy, test_state = sess.run([model.accuracy, model.final_state], feed_dict=feed)
    test_acc.append(batch_accuracy)
print("Test accuracy: {:.4f}".format(np.mean(test_acc)))
