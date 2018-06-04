import os

for i in range(0,45190):
    if ('train_%s.wav.npy' % i not in os.listdir('asset/data/preprocess/mfcc/')):
        print(i)