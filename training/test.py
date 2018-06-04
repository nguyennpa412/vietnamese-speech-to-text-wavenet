import sugartensor as tf
from data import SpeechCorpus, voca_size
from model import *
import numpy as np
from tqdm import tqdm
import pandas as pd
import os
from shutil import copyfile

train_path = './asset/train/'
best_model = './best_model/'

# set log level to debug
tf.sg_verbosity(10)

# command line argument for set_name
tf.sg_arg_def(set=('test', "'train', 'valid', or 'test'.  The default is 'valid'"))
tf.sg_arg_def(frac=(1.0, "test fraction ratio to whole data set. The default is 1.0(=whole set)"))


#
# hyper parameters
#

# batch size
batch_size = 16

#
# inputs
#

# corpus input tensor ( with QueueRunner )
data = SpeechCorpus(batch_size=batch_size, set_name=tf.sg_arg().set)

# mfcc feature of audio
x = data.mfcc
# target sentence label
y = data.label

# sequence length except zero-padding
seq_len = tf.not_equal(x.sg_sum(axis=2), 0.).sg_int().sg_sum(axis=1)

#
# Testing Graph
#

# encode audio feature
logit = get_logit(x, voca_size=voca_size)

# CTC loss
loss = logit.sg_ctc(target=y, seq_len=seq_len)

#
# run network
#

with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:

    # init variables
    tf.sg_init(sess)

    # restore parameters
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint('asset/train'))

    # logging
    tf.sg_info('Testing started on %s set at global step[%08d].' %
            (tf.sg_arg().set.upper(), sess.run(tf.sg_global_step())))

    with tf.sg_queue_context():

        # create progress bar
        iterator = tqdm(range(0, int(data.num_batch * tf.sg_arg().frac)), total=int(data.num_batch * tf.sg_arg().frac),
                        initial=0, desc='test', ncols=70, unit='b', leave=False)

        # batch loop
        loss_avg = 0.
        for _ in iterator:

            # run session
            batch_loss = sess.run(loss)

            # loss history update
            if batch_loss is not None and \
                    not np.isnan(batch_loss.all()) and not np.isinf(batch_loss.all()):
                loss_avg += np.mean(batch_loss)

        # final average
        loss_avg /= data.num_batch * tf.sg_arg().frac

    # logging
    tf.sg_info('Testing finished on %s.(CTC loss=%f)' % (tf.sg_arg().set.upper(), loss_avg))

    if 'loss.csv' not in os.listdir('.'):
        loss = pd.DataFrame({'Epoch': [], 'Step': [], 'Testing_loss': []})
        loss.to_csv('loss.csv')

    global_step = sess.run(tf.sg_global_step())
    pf = pd.read_csv('loss.csv')
    pf_data = pf.values.T.tolist()[1:]
    if (global_step % 2823 == 0):
        epoch = global_step / 2823 - 1
    else:
        epoch = global_step / 2823

    if (len(pf_data[2]) < 1):
        pf_data[0].append(epoch)
        pf_data[1].append(global_step)
        pf_data[2].append(loss_avg)
        loss_data = pd.DataFrame({'Epoch':pf_data[0], 'Step':pf_data[1], 'Testing_loss':pf_data[2]})
        loss_data.to_csv('loss.csv')

        copyfile(train_path + 'checkpoint', best_model + 'checkpoint')
        copyfile(   train_path + 'model.ckpt-%d.data-00000-of-00001' % pf_data[1][0], 
                    best_model + 'model.ckpt-%d.data-00000-of-00001' % pf_data[1][0]  )
        copyfile(   train_path + 'model.ckpt-%d.index' % pf_data[1][0], 
                    best_model + 'model.ckpt-%d.index' % pf_data[1][0]  )
        copyfile(   train_path + 'model.ckpt-%d.meta' % pf_data[1][0], 
                    best_model + 'model.ckpt-%d.meta' % pf_data[1][0]  )
    else:
        min = pf_data[2][0]
        for i in range(0,len(pf_data[2])):
            if (pf_data[2][i] < min):
                min = pf_data[2][i]

        pf_data[0].append(epoch)
        pf_data[1].append(global_step)
        pf_data[2].append(loss_avg)
        loss_data = pd.DataFrame({'Epoch':pf_data[0], 'Step':pf_data[1], 'Testing_loss':pf_data[2]})
        loss_data.to_csv('loss.csv')

        if (loss_avg < min):
            for file in os.listdir(best_model):
                os.remove(best_model + file)

            copyfile(train_path + 'checkpoint', best_model + 'checkpoint')
            copyfile(   train_path + 'model.ckpt-%d.data-00000-of-00001' % global_step, 
                        best_model + 'model.ckpt-%d.data-00000-of-00001' % global_step  )
            copyfile(   train_path + 'model.ckpt-%d.index' % global_step, 
                        best_model + 'model.ckpt-%d.index' % global_step  )
            copyfile(   train_path + 'model.ckpt-%d.meta' % global_step, 
                        best_model + 'model.ckpt-%d.meta' % global_step  )

    