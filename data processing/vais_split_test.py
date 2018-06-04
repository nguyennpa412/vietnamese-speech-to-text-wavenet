import os
import shutil

train_folder = './asset/data/vais/train/audio/'
train_text = './asset/data/vais/train/text.txt'

test_folder = './asset/data/vais/test/audio/'
test_text = './asset/data/vais/test/text.txt'

trainText = open(train_text, 'rt')
recordsTrainText = trainText.readlines()

testText = open(test_text, 'w+')

count = 0

for record in recordsTrainText:
    if (count < 100):
        splitted = record.split('|')
        audioName = splitted[0] + '.wav'
        shutil.move(train_folder + audioName, test_folder + audioName)
        print(audioName)
        count += 1