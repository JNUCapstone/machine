import tensorflow as tf
import numpy as np

char_set = ['h','e','l','o']

x_one_hot = [[
[1,0,0,0],
[0,1,0,0],
[0,0,1,0],
[0,0,1,0]
]]
y_data = [[1,2,2,3]]

num_classes = 4
input_dim = 4
hidden_size = 12
batch_size = 1
sequence_length = 4
learning_rate = 0.1

X = tf.placeholder(
    tf.float32, [None, sequence_length, input_dim])
Y = tf.placeholder(tf.int32, [None, sequence_length])

cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_size, state_is_tuple=True)

initial_state = cell.zero_state(batch_size, tf.float32)

outputs, _states = tf.nn.dynamic_rnn(cell, X, initial_state = initial_state, dtype=tf.float32)

X_for_fc = tf.reshape(outputs, [-1, hidden_size])

outputs = tf.contrib.layers.fully_connected(inputs=X_for_fc, num_outputs=num_classes, activation_fn=None)

outputs = tf.reshape(outputs, [batch_size, sequence_length, num_classes])

weights = tf.ones([batch_size, sequence_length])

sequence_loss = tf.contrib.seq2seq.sequence_loss(logits=outputs, target=Y, weights=weights)

loss = tf.reduce_mean(sequence_loss)

train = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(loss)

prediction = tf.argmax(outputs, axis=2)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for i in range(50):
        l , _ = sess.run([loss, train], feed_dict={X: x_one_hot, Y: y_data})
        result = sess.run(prediction, feed_dict={X: x_one_hot})
        print(i, "loss:", l, "prediction: ", result, "true Y: ", y_data)

        result_str = [char_set[c] for c in np.squeeze(result)]
        print("\tPrediction str: ", "".join(result_str))
