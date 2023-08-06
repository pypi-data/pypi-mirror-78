# flake8: noqa
from tensorflow.examples.tutorials.mnist import input_data

import numpy as np
import tensorflow as tf


def save():
  mnist = input_data.read_data_sets('data', one_hot=True)

  # Create the model
  x = tf.placeholder(tf.float32, [None, 784], name="inputs")
  l1 = tf.layers.dense(x, 128, activation=tf.nn.elu, name='l1')
  l2 = tf.layers.dense(l1, 128, activation=tf.nn.elu, name='l2')
  y = tf.layers.dense(l2, 10, activation=tf.nn.sigmoid, name='y')
  logits = tf.identity(y, name='logits')

  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 10])

  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  num_epochs = 1000
  report_every = 100

  with tf.Session() as sess:
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())

    train_fetch = {'train': train_step}
    test_fetch = {'train': train_step, 'accuracy': accuracy}

    for i in range(1, 1 + num_epochs):

      if i % report_every == 0:
        fd = {x: mnist.test.images, y_: mnist.test.labels}
        v = sess.run(test_fetch, feed_dict=fd)
        print(i, v['accuracy'])
      else:
        batch_xs, batch_ys = mnist.train.next_batch(100)
        v = sess.run(train_fetch, feed_dict={x: batch_xs, y_: batch_ys})

    saver.save(sess, './mnist_model', global_step=i)


def load():
  mnist = input_data.read_data_sets('data', one_hot=True)

  with tf.Session() as sess:
    saver = tf.train.import_meta_graph('mnist_model-100.meta')
    saver.restore(sess, tf.train.latest_checkpoint('./'))

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name('inputs:0')
    y = graph.get_tensor_by_name('logits:0')

    num_test = 10
    batch_xs = mnist.test.images[:num_test]
    batch_ys = mnist.test.labels[:num_test]
    logits = sess.run(y, {x: batch_xs})
    prediction = np.argmax(logits, axis=1)
    truth = np.argmax(batch_ys, axis=1)
    confidence = np.max(logits, axis=1) / np.sum(logits, axis=1)

    for i in range(num_test):
      print(prediction[i], truth[i], confidence[i])

if __name__ == "__main__":
  # save()
  load()
