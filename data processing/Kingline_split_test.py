import os
import shutil

train_audio_folder = './asset/data/King-ASR-M-008-Promotion/train/audio/'
train_text = './asset/data/King-ASR-M-008-Promotion/train/text.txt'
new_train_text = './asset/data/King-ASR-M-008-Promotion/train/new_text.txt'

test_audio_folder = './asset/data/King-ASR-M-008-Promotion/test/audio/'
test_text = './asset/data/King-ASR-M-008-Promotion/test/text.txt'

test_list = []

def getTestAudio(category, part, path):
	des = './asset/data/King-ASR-M-008-Promotion/test/audio/%s/%s/' % (category, part)
	if not os.path.exists(des):
		os.makedirs(des)

	file_list = os.listdir(path)
	total = len(file_list)
	num_test = total/10
	
	for i in range(0,num_test):
		audio = file_list[i]
		test_list.append(audio.split('.')[0])
		shutil.move(path + audio, des + audio)

def getTestText():
	train = open(train_text, 'r')
	records = train.readlines()

	new_train = open(new_train_text, 'w+')
	test = open(test_text, 'w+')

	count = 0
	print(test_list)
	for record in records:
		audio_name = record.split('|')[0]

		if (audio_name in test_list):
			test.write(record)
			print(audio_name + '-> TEST %d' % count)
			count += 1
		else:
			new_train.write(record)
	
	train.close()
	new_train.close()
	test.close()
	print(count)

def reMove(category, part, path):
	des = './asset/data/King-ASR-M-008-Promotion/train/audio/%s/%s/' % (category, part)

	for audio in os.listdir(path):
		shutil.move(path + audio, des + audio)

for category in os.listdir(train_audio_folder):
	path = train_audio_folder + category + '/'
	for part in os.listdir(path):
		getTestAudio(category, part, path + part + '/')

getTestText()

# for category in os.listdir(test_audio_folder):
# 	path = test_audio_folder + category + '/'
# 	for part in os.listdir(path):
# 		reMove(category, part, path + part + '/')