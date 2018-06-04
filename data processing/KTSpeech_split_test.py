import os
import shutil

train_folder = './asset/data/KTSpeech/train/audio/'

test_folder = './asset/data/KTSpeech/test/audio/'
test_text = './asset/data/KTSpeech/test/text.txt'

testText = open(test_text, 'rt')
recordsTestText = testText.readlines()

count = 0

for record in recordsTestText:
    splitted = record.split('|')
    audioName = splitted[0].upper() + '.wav'
    shutil.move(train_folder + audioName, test_folder + audioName)
    print(audioName)