import wave
import contextlib
import datetime
import os

train_folder = './asset/data/FINAL_DATA/train/audio/'
test_folder = './asset/data/FINAL_DATA/test/audio/'

def measureDuration(path, category):
    total = 0
    count = 0
    for audio in os.listdir(path):
        if ('wav' in audio):
            with contextlib.closing(wave.open(path + audio,'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                total += duration
                count += 1

    print('%s set: %d - %s' % (category, count, str(datetime.timedelta(seconds=total))))

measureDuration(train_folder, 'train')
measureDuration(test_folder, 'test')