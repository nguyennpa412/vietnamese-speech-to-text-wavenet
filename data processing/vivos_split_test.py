import os
import shutil

train_audio_folder = './asset/data/vivos/train/waves/'
train_text = './asset/data/vivos/train/old_prompts.txt'
new_train_text = './asset/data/vivos/train/prompts.txt'

test_audio_folder = './asset/data/vivos/test/waves/'
test_text = './asset/data/vivos/test/prompts.txt'

test_list = []

def getTestAudio(category, path):
	des = './asset/data/vivos/test/waves/%s/' % category
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
		audio_name = record.split(' ')[0]

		if (audio_name.upper() in test_list):
			test.write(record)
			print(audio_name + '-> TEST %d' % count)
			count += 1
		else:
			new_train.write(record)
	
	train.close()
	new_train.close()
	test.close()

for category in os.listdir(train_audio_folder):
	getTestAudio(category, train_audio_folder + category + '/')

getTestText()