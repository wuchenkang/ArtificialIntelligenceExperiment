import tensorflow as tf
import numpy as np
import csv


# 从csv文件加载训练集
def readData(file_name):
    data_set = []
    data_file = open(file_name, "r", encoding="utf-8")
    data_csv = csv.reader(data_file)
    for row in data_csv:
        data_set.append(row[:-2]+row[-1:])
    data_file.close()
    data_set = data_set[1:]

    for row in data_set:
        for col in range(len(row)):
            row[col] = float(row[col])
    return data_set


# 提取数据
def processData(data_set, split_rate):
    x = np.zeros((len(data_set), len(data_set[0])-1), dtype=float)
    for i in range(len(data_set)):
        for j in range(len(data_set[0])-1):
            x[i][j] = data_set[i][j]

    y = [data_set[i][-1] for i in range(len(data_set))]
    y = np.array(y)

    split_idx = int(len(x) * split_rate)
    train_x, valid_x = x[:split_idx], x[split_idx:]
    train_y, valid_y = y[:split_idx], y[split_idx:]

    return (train_x, train_y), (valid_x, valid_y)


def setEnv(data_size, x_dim, y_dim):
    global INPUT_SIZE, OUTPUT_SIZE, TIME_STEPS, BATCH_SIZE, CELL_SIZE, LEARNING_RATE
    CELL_SIZE = 128
    INPUT_SIZE = x_dim
    OUTPUT_SIZE = y_dim
    TIME_STEPS = 200
    BATCH_SIZE = data_size // TIME_STEPS
    CELL_SIZE = 128
    LEARNING_RATE = 0.01


def getBatch(x_in, y_in):
    x_out = x_in.reshape(-1, TIME_STEPS, INPUT_SIZE)
    y_out = y_in.reshape(-1, TIME_STEPS, OUTPUT_SIZE)
    return x_out, y_out


class LSTMRNN():
    def __init__(self, time_steps, input_size, output_size, cell_size, batch_size):
        self.time_steps = time_steps
        self.input_size = input_size
        self.output_size = output_size
        self.cell_size = cell_size
        self.batch_size = batch_size

        with tf.name_scope('inputs'):
            self.xs = tf.placeholder(tf.float32, [None, time_steps, input_size], name='xs')
            self.ys = tf.placeholder(tf.float32, [None, time_steps, output_size], name='ys')

        with tf.variable_scope('in_hidden'):
            self.add_input_layer()

        with tf.variable_scope('LSTM_cell'):
            self.add_cell()

        with tf.variable_scope('out_hidden'):
            self.add_output_layer()

        with tf.name_scope('cost'):
            self.compute_cost()

        with tf.name_scope('train'):
            self.train_op = tf.train.AdamOptimizer(LEARNING_RATE).minimize(self.cost)

    def add_input_layer(self):
        xs_in = tf.reshape(self.xs, [-1, self.input_size], name='3D_TO_2D')
        Ws_in = self._weight_variable([self.input_size, self.cell_size])
        bs_in = self._bias_variable([self.cell_size, ])
        with tf.name_scope('Wx_Plus_b'):
            ys_in = tf.matmul(xs_in, Ws_in) + bs_in
        self.ys_in = tf.reshape(ys_in, [-1, self.time_steps, self.cell_size], name='2D_TO_3D')

    def add_cell(self):
        self.lstm_cell = tf.contrib.rnn.BasicLSTMCell(self.cell_size, forget_bias=1.0, state_is_tuple=True)
        with tf.name_scope('initial_state'):
            self.cell_init_state = self.lstm_cell.zero_state(self.batch_size, dtype=tf.float32)
        self.cell_outputs, self.cell_final_state = tf.nn.dynamic_rnn(
            self.lstm_cell, self.ys_in, initial_state=self.cell_init_state, time_major=False)

    def add_output_layer(self):
        xs_out = tf.reshape(self.cell_outputs, [-1, self.cell_size], name='3D_2_2D')
        Ws_out = self._weight_variable([self.cell_size, self.output_size])
        bs_out = self._bias_variable([self.output_size, ])
        # shape = (batch * steps, output_size)
        with tf.name_scope('Wx_plus_b'):
            self.ys_out = tf.matmul(xs_out, Ws_out) + bs_out

    def compute_cost(self):
        losses = tf.contrib.legacy_seq2seq.sequence_loss_by_example(
            [tf.reshape(self.ys_out, [-1], name='reshape_pred')],
            [tf.reshape(self.ys, [-1], name='reshape_target')],
            [tf.ones([self.batch_size * self.time_steps], dtype=tf.float32)],
            average_across_timesteps=True,
            softmax_loss_function=self.ms_error,
            name='losses'
        )
        with tf.name_scope('average_cost'):
            self.cost = tf.div(
                tf.reduce_sum(losses, name='losses_sum'),
                self.batch_size,
                name='average_cost')
            tf.summary.scalar('cost', self.cost)

    @staticmethod
    def ms_error(labels, logits):
        return tf.square(tf.subtract(labels, logits))

    def _weight_variable(self, shape, name='weights'):
        initializer = tf.random_normal_initializer(mean=0., stddev=1., )
        return tf.get_variable(shape=shape, initializer=initializer, name=name)

    def _bias_variable(self, shape, name='biases'):
        initializer = tf.constant_initializer(0.1)
        return tf.get_variable(name=name, shape=shape, initializer=initializer)


if __name__ == '__main__':
    data_set = readData("train.csv")
    train_set, valid_set = processData(data_set, 0.5)
    setEnv(len(train_set[0]), len(data_set[0])-1, 1)
    model = LSTMRNN(TIME_STEPS, INPUT_SIZE, OUTPUT_SIZE, CELL_SIZE, BATCH_SIZE)
    sess = tf.Session()
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs", sess.graph)
    init = tf.global_variables_initializer()
    sess.run(init)
    seq, res = getBatch(train_set[0], train_set[1])
    for i in range(500):
        if i == 0:
            feed_dict = {
                    model.xs: seq,
                    model.ys: res,
                    # create initial state
            }
        else:
            feed_dict = {
                model.xs: seq,
                model.ys: res,
                model.cell_init_state: state
            }

        _, cost, state, pred = sess.run([model.train_op, model.cost, model.cell_final_state, model.ys_out], feed_dict=feed_dict)
        if i % 20 == 0:
            print('cost: ', round(cost, 4))
            result = sess.run(merged, feed_dict)
            writer.add_summary(result, i)


