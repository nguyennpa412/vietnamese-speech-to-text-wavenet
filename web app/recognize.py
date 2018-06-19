# -*- coding: utf-8 -*-
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import sugartensor as tf
import numpy as np
import librosa
from model import *
import data

# set log level to debug
tf.sg_verbosity(10)

#
# hyper parameters
#

batch_size = 1     # batch size

#
# inputs
#

# vocabulary size
voca_size = data.voca_size

# mfcc feature of audio
x = tf.placeholder(dtype=tf.sg_floatx, shape=(batch_size, None, 20))

# sequence length except zero-padding
seq_len = tf.not_equal(x.sg_sum(axis=2), 0.).sg_int().sg_sum(axis=1)

# encode audio feature
logit = get_logit(x, voca_size=voca_size)

# ctc decoding
decoded, _ = tf.nn.ctc_beam_search_decoder(logit.sg_transpose(perm=[1, 0, 2]), seq_len, merge_repeated=False)

# to dense tensor
y = tf.sparse_to_dense(decoded[0].indices, decoded[0].dense_shape, decoded[0].values) + 1

#
# regcognize wave file
#

# command line argument for input wave file path
tf.sg_arg_def(file=('', 'speech wave file to recognize.'))

# load wave file
wav, _ = librosa.load(tf.sg_arg().file, mono=True, sr=16000)
# get mfcc feature
mfcc = np.transpose(np.expand_dims(librosa.feature.mfcc(wav, 16000), axis=0), [0, 2, 1])

print('\n Recognizing... \n')

# run network
with tf.Session() as sess:

    # init variables
    tf.sg_init(sess)

    # restore parameters
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint('asset/train'))
    # run session
    label = sess.run(y, feed_dict={x: mfcc})

    # print label
    data.print_index(label)

    for index_list in label:
        output = data.index2str(index_list)

print('\n Wavenet result: \n' + output + '\n')
filetype = sys.argv[3]
outputfile = open('res_wavenet_%s.txt' % filetype, 'w')
outputfile.write(output)
outputfile.close()